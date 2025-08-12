#!/usr/bin/env python3
"""
MLflow Model Upload Monitoring Script
====================================

This script monitors MLflow model uploads and alerts on failures:
1. Checks recent runs for upload failures
2. Monitors artifact storage connectivity
3. Alerts on configuration issues
4. Generates health reports
5. Can be scheduled to run periodically

Usage:
    python mlflow_monitor.py           # Run once
    python mlflow_monitor.py --watch   # Run continuously (every 5 minutes)
    python mlflow_monitor.py --report  # Generate detailed report

Author: MLflow Monitoring System
Purpose: Prevent and detect tourism_recommendation_pipeline model upload failures
"""

import os
import sys
import json
import time
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv

# Configure logging
def setup_logging():
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    
    # Also log to file
    file_handler = logging.FileHandler('mlflow_monitor.log')
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)
    
    return logging.getLogger(__name__)

logger = setup_logging()

class MLflowHealthMonitor:
    """Monitor MLflow system health and model upload status."""
    
    def __init__(self):
        self.setup_environment()
        self.client = None
        self.s3_client = None
        self.alerts = []
        
    def setup_environment(self):
        """Setup MLflow environment."""
        load_dotenv('.env')
        
        import mlflow
        mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
        
        # Set S3 environment variables
        os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
        os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
        os.environ['MLFLOW_S3_ENDPOINT_URL'] = os.getenv('MLFLOW_S3_ENDPOINT_URL')
        
    def check_dependencies(self) -> bool:
        """Check if critical dependencies are available."""
        try:
            import mlflow
            import boto3
            import requests
            return True
        except ImportError as e:
            logger.error(f"❌ Missing dependency: {e}")
            self.alerts.append(f"Missing dependency: {e}")
            return False
            
    def get_mlflow_client(self):
        """Get or create MLflow client."""
        if not self.client:
            try:
                import mlflow
                self.client = mlflow.MlflowClient()
            except Exception as e:
                logger.error(f"❌ Failed to create MLflow client: {e}")
                self.alerts.append(f"MLflow client creation failed: {e}")
                return None
        return self.client
        
    def get_s3_client(self):
        """Get or create S3 client."""
        if not self.s3_client:
            try:
                import boto3
                self.s3_client = boto3.client(
                    's3',
                    endpoint_url=os.getenv('MLFLOW_S3_ENDPOINT_URL'),
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    region_name='us-east-1'
                )
            except Exception as e:
                logger.error(f"❌ Failed to create S3 client: {e}")
                self.alerts.append(f"S3 client creation failed: {e}")
                return None
        return self.s3_client
        
    def check_mlflow_connectivity(self) -> bool:
        """Test MLflow server connectivity."""
        client = self.get_mlflow_client()
        if not client:
            return False
            
        try:
            experiments = client.search_experiments()
            logger.info(f"✅ MLflow connectivity OK - {len(experiments)} experiments found")
            return True
        except Exception as e:
            logger.error(f"❌ MLflow connectivity failed: {e}")
            self.alerts.append(f"MLflow connectivity failed: {e}")
            return False
            
    def check_s3_connectivity(self) -> bool:
        """Test S3/MinIO storage connectivity."""
        s3_client = self.get_s3_client()
        if not s3_client:
            return False
            
        try:
            buckets = s3_client.list_buckets()
            logger.info(f"✅ S3 connectivity OK - {len(buckets['Buckets'])} buckets found")
            
            # Test write/read permissions on mlflow bucket
            test_key = f'health-check-{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt'
            s3_client.put_object(Bucket='mlflow', Key=test_key, Body=b'health check')
            s3_client.delete_object(Bucket='mlflow', Key=test_key)
            logger.info("✅ S3 read/write permissions OK")
            return True
            
        except Exception as e:
            logger.error(f"❌ S3 connectivity failed: {e}")
            self.alerts.append(f"S3 connectivity failed: {e}")
            return False
            
    def check_recent_runs(self, hours: int = 24) -> Dict:
        """Check recent runs for issues."""
        client = self.get_mlflow_client()
        if not client:
            return {"status": "error", "message": "No MLflow client"}
            
        try:
            # Focus on tourism experiments
            experiments = ['tourism_recommendation_enhanced', 'wdr_tourism_recommendation_models']
            all_runs = []
            
            for exp_name in experiments:
                try:
                    exp = client.get_experiment_by_name(exp_name)
                    if exp:
                        since_time = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
                        runs = client.search_runs(
                            exp.experiment_id,
                            filter_string=f"attribute.start_time > {since_time}",
                            max_results=100
                        )
                        all_runs.extend([(exp_name, run) for run in runs])
                except Exception as e:
                    logger.warning(f"⚠️ Could not check experiment {exp_name}: {e}")
                    
            if not all_runs:
                logger.info("ℹ️ No recent runs found")
                return {"status": "no_runs", "runs": []}
                
            # Analyze runs
            run_issues = []
            status_counts = {}
            
            for exp_name, run in all_runs:
                status = run.info.status
                name = run.data.tags.get('mlflow.runName', 'Unknown')
                run_id = run.info.run_id
                
                status_counts[status] = status_counts.get(status, 0) + 1
                
                # Check for artifacts
                try:
                    artifacts = client.list_artifacts(run_id)
                    if len(artifacts) == 0 and status == 'FINISHED':
                        issue = {
                            'experiment': exp_name,
                            'run_name': name,
                            'run_id': run_id[:8],
                            'issue': 'No artifacts found',
                            'status': status,
                            'start_time': datetime.fromtimestamp(run.info.start_time / 1000)
                        }
                        run_issues.append(issue)
                        logger.warning(f"⚠️ {exp_name}/{name}: No artifacts found")
                        
                except Exception as artifact_e:
                    issue = {
                        'experiment': exp_name,
                        'run_name': name,
                        'run_id': run_id[:8],
                        'issue': f'Artifact access failed: {artifact_e}',
                        'status': status,
                        'start_time': datetime.fromtimestamp(run.info.start_time / 1000)
                    }
                    run_issues.append(issue)
                    logger.error(f"❌ {exp_name}/{name}: Artifact access failed - {artifact_e}")
                    
            logger.info(f"📊 Recent runs ({hours}h): {sum(status_counts.values())} total")
            for status, count in status_counts.items():
                logger.info(f"  {status}: {count}")
                
            if run_issues:
                logger.warning(f"⚠️ Found {len(run_issues)} runs with issues")
                self.alerts.extend([f"Run issue: {issue['experiment']}/{issue['run_name']} - {issue['issue']}" for issue in run_issues])
                
            return {
                "status": "success",
                "total_runs": sum(status_counts.values()),
                "status_counts": status_counts,
                "issues": run_issues
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to check recent runs: {e}")
            self.alerts.append(f"Failed to check recent runs: {e}")
            return {"status": "error", "message": str(e)}
            
    def check_model_registry(self) -> Dict:
        """Check model registry status."""
        client = self.get_mlflow_client()
        if not client:
            return {"status": "error", "message": "No MLflow client"}
            
        try:
            models = client.search_registered_models()
            tourism_models = [m for m in models if 'tourism' in m.name.lower()]
            
            model_issues = []
            ready_count = 0
            total_versions = 0
            
            for model in tourism_models:
                for version in model.latest_versions:
                    total_versions += 1
                    if version.status == "READY":
                        ready_count += 1
                    else:
                        issue = {
                            'model_name': model.name,
                            'version': version.version,
                            'status': version.status,
                            'stage': version.current_stage or 'None'
                        }
                        model_issues.append(issue)
                        logger.warning(f"⚠️ Model {model.name} v{version.version}: {version.status}")
                        
            logger.info(f"📦 Model registry: {len(tourism_models)} models, {ready_count}/{total_versions} versions ready")
            
            if model_issues:
                self.alerts.extend([f"Model issue: {issue['model_name']} v{issue['version']} - {issue['status']}" for issue in model_issues])
                
            return {
                "status": "success",
                "total_models": len(tourism_models),
                "total_versions": total_versions,
                "ready_versions": ready_count,
                "issues": model_issues
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to check model registry: {e}")
            self.alerts.append(f"Failed to check model registry: {e}")
            return {"status": "error", "message": str(e)}
            
    def generate_health_report(self) -> Dict:
        """Generate comprehensive health report."""
        logger.info("🔍 Generating health report...")
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "alerts": [],
            "summary": {}
        }
        
        # Run all checks
        checks = [
            ("dependencies", self.check_dependencies),
            ("mlflow_connectivity", self.check_mlflow_connectivity),
            ("s3_connectivity", self.check_s3_connectivity)
        ]
        
        for check_name, check_func in checks:
            try:
                report["checks"][check_name] = check_func()
            except Exception as e:
                report["checks"][check_name] = False
                logger.error(f"❌ Check {check_name} failed: {e}")
                
        # Check runs and models
        report["checks"]["recent_runs"] = self.check_recent_runs()
        report["checks"]["model_registry"] = self.check_model_registry()
        
        # Collect alerts
        report["alerts"] = self.alerts.copy()
        
        # Generate summary
        all_basic_checks = all(report["checks"][check] for check in ["dependencies", "mlflow_connectivity", "s3_connectivity"])
        run_status = report["checks"]["recent_runs"]["status"] == "success"
        model_status = report["checks"]["model_registry"]["status"] == "success"
        
        report["summary"] = {
            "overall_health": "healthy" if all_basic_checks and not self.alerts else "issues_detected",
            "basic_connectivity": "ok" if all_basic_checks else "failed",
            "recent_runs_ok": run_status,
            "model_registry_ok": model_status,
            "total_alerts": len(self.alerts)
        }
        
        return report
        
    def save_report(self, report: Dict, filename: str = None):
        """Save health report to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mlflow_health_report_{timestamp}.json"
            
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"📄 Health report saved to {filename}")
        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")
            
    def print_summary(self, report: Dict):
        """Print health report summary."""
        logger.info("="*60)
        logger.info("📊 MLFLOW HEALTH SUMMARY")
        logger.info("="*60)
        
        summary = report["summary"]
        
        # Overall status
        status_emoji = "✅" if summary["overall_health"] == "healthy" else "⚠️"
        logger.info(f"Overall Health: {status_emoji} {summary['overall_health'].upper()}")
        
        # Basic checks
        basic_status = "✅ PASS" if summary["basic_connectivity"] == "ok" else "❌ FAIL"
        logger.info(f"Basic Connectivity: {basic_status}")
        
        # Recent runs
        runs_status = "✅ PASS" if summary["recent_runs_ok"] else "❌ ISSUES"
        logger.info(f"Recent Runs: {runs_status}")
        
        # Model registry
        models_status = "✅ PASS" if summary["model_registry_ok"] else "❌ ISSUES"
        logger.info(f"Model Registry: {models_status}")
        
        # Alerts
        if report["alerts"]:
            logger.info(f"🚨 ALERTS ({len(report['alerts'])}):")
            for alert in report["alerts"][:5]:  # Show first 5 alerts
                logger.info(f"  • {alert}")
            if len(report["alerts"]) > 5:
                logger.info(f"  ... and {len(report['alerts']) - 5} more")
        else:
            logger.info("🎉 No alerts!")
            
        logger.info("="*60)

def main():
    """Main monitoring function."""
    parser = argparse.ArgumentParser(description="MLflow Health Monitor")
    parser.add_argument('--watch', action='store_true', help='Run continuously every 5 minutes')
    parser.add_argument('--report', action='store_true', help='Generate detailed report file')
    parser.add_argument('--hours', type=int, default=24, help='Hours to look back for run analysis (default: 24)')
    
    args = parser.parse_args()
    
    monitor = MLflowHealthMonitor()
    
    def run_check():
        logger.info(f"🚀 Starting MLflow health check... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        monitor.alerts.clear()  # Clear previous alerts
        
        report = monitor.generate_health_report()
        monitor.print_summary(report)
        
        if args.report:
            monitor.save_report(report)
            
        return report["summary"]["overall_health"] == "healthy"
    
    if args.watch:
        logger.info("👀 Starting continuous monitoring (every 5 minutes)...")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                healthy = run_check()
                if not healthy:
                    logger.warning("⚠️ Health check detected issues!")
                    
                logger.info("⏰ Sleeping for 5 minutes...")
                time.sleep(300)  # 5 minutes
                
        except KeyboardInterrupt:
            logger.info("👋 Monitoring stopped by user")
    else:
        # Run once
        healthy = run_check()
        sys.exit(0 if healthy else 1)

if __name__ == "__main__":
    main()