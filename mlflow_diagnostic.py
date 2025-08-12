#!/usr/bin/env python3
"""
MLflow Model Upload Diagnostic Script
====================================

This script diagnoses MLflow model upload failures by:
1. Testing MLflow server connectivity
2. Verifying S3/MinIO storage connectivity and permissions
3. Running a simple model upload test
4. Analyzing existing experiments and runs
5. Checking for common configuration issues

Author: MLflow Diagnostics
Purpose: Troubleshoot tourism_recommendation_pipeline model upload failures
"""

import os
import sys
import traceback
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed."""
    logger.info("🔍 Checking dependencies...")
    
    missing_deps = []
    required_packages = ['mlflow', 'boto3', 'pandas', 'sklearn', 'numpy']
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} is available")
        except ImportError:
            missing_deps.append(package)
            logger.error(f"❌ {package} is missing")
    
    if missing_deps:
        logger.error(f"Missing dependencies: {missing_deps}")
        return False
    
    return True

def setup_environment():
    """Setup MLflow environment and configuration."""
    logger.info("🔧 Setting up MLflow environment...")
    
    # Load environment variables
    load_dotenv('.env')
    
    # Check required environment variables
    required_vars = [
        'MLFLOW_TRACKING_URI',
        'AWS_ACCESS_KEY_ID', 
        'AWS_SECRET_ACCESS_KEY',
        'MLFLOW_S3_ENDPOINT_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
            logger.error(f"❌ {var} is not set")
        else:
            logger.info(f"✅ {var} is set")
            
    if missing_vars:
        logger.error(f"Missing environment variables: {missing_vars}")
        return False
        
    # Set MLflow configuration
    import mlflow
    mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
    
    # Set S3 environment variables for MLflow
    os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
    os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY') 
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = os.getenv('MLFLOW_S3_ENDPOINT_URL')
    
    logger.info(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")
    return True

def test_mlflow_connectivity():
    """Test connectivity to MLflow tracking server."""
    logger.info("🌐 Testing MLflow server connectivity...")
    
    try:
        import mlflow
        client = mlflow.MlflowClient()
        
        # Test basic operations
        experiments = client.search_experiments()
        logger.info(f"✅ Connected to MLflow server! Found {len(experiments)} experiments")
        
        # List relevant experiments
        tourism_experiments = [exp for exp in experiments if 'tourism' in exp.name.lower()]
        logger.info(f"Tourism-related experiments: {len(tourism_experiments)}")
        
        for exp in tourism_experiments:
            logger.info(f"  - {exp.name} (ID: {exp.experiment_id})")
            
        return True, client
        
    except Exception as e:
        logger.error(f"❌ MLflow server connection failed: {e}")
        return False, None

def test_s3_connectivity():
    """Test S3/MinIO storage connectivity and permissions."""
    logger.info("💾 Testing S3/MinIO storage connectivity...")
    
    try:
        import boto3
        
        s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('MLFLOW_S3_ENDPOINT_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='us-east-1'
        )
        
        # List buckets
        buckets = s3_client.list_buckets()
        logger.info(f"✅ Connected to S3/MinIO! Found {len(buckets['Buckets'])} buckets")
        
        # Test permissions on each bucket
        permissions_ok = True
        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            logger.info(f"Testing permissions for bucket: {bucket_name}")
            
            try:
                # Test read
                s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
                logger.info(f"  ✅ Read permission OK")
                
                # Test write
                test_key = f'diagnostic-test-{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt'
                s3_client.put_object(Bucket=bucket_name, Key=test_key, Body=b'MLflow diagnostic test')
                logger.info(f"  ✅ Write permission OK")
                
                # Test delete
                s3_client.delete_object(Bucket=bucket_name, Key=test_key)
                logger.info(f"  ✅ Delete permission OK")
                
            except Exception as bucket_e:
                logger.error(f"  ❌ Bucket {bucket_name} permission error: {bucket_e}")
                permissions_ok = False
                
        return permissions_ok, s3_client
        
    except Exception as e:
        logger.error(f"❌ S3/MinIO connection failed: {e}")
        return False, None

def analyze_existing_runs(client):
    """Analyze existing MLflow runs for issues."""
    logger.info("🔍 Analyzing existing runs...")
    
    try:
        # Focus on tourism_recommendation_enhanced experiment
        exp = client.get_experiment_by_name('tourism_recommendation_enhanced')
        if not exp:
            logger.warning("tourism_recommendation_enhanced experiment not found")
            return
            
        # Get recent runs (last 7 days)
        since_time = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
        runs = client.search_runs(
            exp.experiment_id,
            filter_string=f"attribute.start_time > {since_time}",
            max_results=50,
            order_by=['attribute.start_time DESC']
        )
        
        logger.info(f"Found {len(runs)} runs in the last 7 days")
        
        # Analyze run statuses
        status_counts = {}
        artifact_issues = []
        
        for run in runs:
            status = run.info.status
            name = run.data.tags.get('mlflow.runName', 'Unknown')
            
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Check artifacts
            try:
                artifacts = client.list_artifacts(run.info.run_id)
                if len(artifacts) == 0:
                    artifact_issues.append((name, run.info.run_id, "No artifacts found"))
                    logger.warning(f"  ❌ {name}: No artifacts found")
                else:
                    logger.info(f"  ✅ {name}: {len(artifacts)} artifacts found")
                    
            except Exception as artifact_e:
                artifact_issues.append((name, run.info.run_id, str(artifact_e)))
                logger.error(f"  ❌ {name}: Artifact access failed - {artifact_e}")
        
        # Summary
        logger.info("📊 Run Status Summary:")
        for status, count in status_counts.items():
            logger.info(f"  {status}: {count} runs")
            
        if artifact_issues:
            logger.warning(f"📦 Artifact Issues Found: {len(artifact_issues)} runs with problems")
            for name, run_id, issue in artifact_issues[:5]:  # Show first 5
                logger.warning(f"  - {name} ({run_id[:8]}...): {issue}")
                
        return len(artifact_issues) == 0
        
    except Exception as e:
        logger.error(f"❌ Failed to analyze existing runs: {e}")
        return False

def test_model_upload():
    """Test a simple model upload to reproduce the issue."""
    logger.info("🧪 Testing model upload...")
    
    try:
        import mlflow
        import mlflow.sklearn
        from sklearn.linear_model import LinearRegression
        import numpy as np
        
        # Create a simple test model
        X = np.random.randn(100, 5)
        y = np.random.randn(100)
        model = LinearRegression()
        model.fit(X, y)
        
        # Start an MLflow run
        with mlflow.start_run(run_name="diagnostic_test_model"):
            # Log parameters
            mlflow.log_param("test_param", "diagnostic_test")
            mlflow.log_metric("test_metric", 0.95)
            
            # Try to log the model
            try:
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="test_model",
                    registered_model_name="diagnostic-test-model"
                )
                logger.info("✅ Model upload successful!")
                return True
                
            except Exception as model_e:
                logger.error(f"❌ Model upload failed: {model_e}")
                logger.error(f"Full error: {traceback.format_exc()}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Test model upload setup failed: {e}")
        return False

def check_registered_models(client):
    """Check status of registered models."""
    logger.info("📋 Checking registered models...")
    
    try:
        models = client.search_registered_models()
        tourism_models = [m for m in models if 'tourism' in m.name.lower() or 'diagnostic' in m.name.lower()]
        
        logger.info(f"Found {len(tourism_models)} relevant registered models:")
        
        for model in tourism_models:
            logger.info(f"  📦 {model.name}")
            for version in model.latest_versions:
                status = version.status
                stage = version.current_stage or "None"
                logger.info(f"    Version {version.version}: {status} (Stage: {stage})")
                
                if status != "READY":
                    logger.warning(f"    ⚠️ Model version {version.version} status: {status}")
                    
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to check registered models: {e}")
        return False

def generate_report():
    """Generate diagnostic report with recommendations."""
    logger.info("📝 Generating diagnostic report...")
    
    report = f"""
MLflow Model Upload Diagnostic Report
=====================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY OF FINDINGS:
"""
    
    # This will be populated by the main function
    return report

def main():
    """Main diagnostic function."""
    logger.info("🚀 Starting MLflow Model Upload Diagnostics...")
    logger.info("="*60)
    
    results = {}
    
    # 1. Check dependencies
    results['dependencies'] = check_dependencies()
    if not results['dependencies']:
        logger.error("❌ Dependency check failed. Please install missing packages.")
        return 1
    
    # 2. Setup environment
    results['environment'] = setup_environment()
    if not results['environment']:
        logger.error("❌ Environment setup failed. Please check your .env file.")
        return 1
        
    # 3. Test MLflow connectivity
    results['mlflow_connectivity'], client = test_mlflow_connectivity()
    if not results['mlflow_connectivity']:
        logger.error("❌ MLflow server connectivity failed.")
        return 1
        
    # 4. Test S3 connectivity
    results['s3_connectivity'], s3_client = test_s3_connectivity()
    if not results['s3_connectivity']:
        logger.error("❌ S3/MinIO connectivity failed.")
        return 1
        
    # 5. Analyze existing runs
    results['existing_runs'] = analyze_existing_runs(client)
    
    # 6. Check registered models
    results['registered_models'] = check_registered_models(client)
    
    # 7. Test model upload
    results['model_upload'] = test_model_upload()
    
    # Generate final report
    logger.info("="*60)
    logger.info("🏁 DIAGNOSTIC RESULTS:")
    logger.info("="*60)
    
    all_passed = True
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{test.replace('_', ' ').title():.<30} {status}")
        if not passed:
            all_passed = False
    
    logger.info("="*60)
    
    if all_passed:
        logger.info("🎉 All diagnostics passed! MLflow should be working correctly.")
        logger.info("💡 If you're still experiencing issues, the problem might be:")
        logger.info("   - Network connectivity issues")
        logger.info("   - Temporary server problems") 
        logger.info("   - Specific model serialization issues")
    else:
        logger.error("⚠️  Some diagnostics failed. Check the errors above.")
        logger.info("💡 RECOMMENDATIONS:")
        
        if not results['dependencies']:
            logger.info("   • Install missing Python packages")
        if not results['environment']:
            logger.info("   • Check .env file configuration")
        if not results['mlflow_connectivity']:
            logger.info("   • Verify MLflow server is running and accessible")
        if not results['s3_connectivity']:
            logger.info("   • Check S3/MinIO credentials and endpoint")
        if not results['existing_runs']:
            logger.info("   • Existing runs have artifact issues - boto3 was likely missing")
        if not results['model_upload']:
            logger.info("   • Model upload is failing - check logs above")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())