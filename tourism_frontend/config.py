import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

# Google Maps Configuration (Basic URLs only - no API key needed)
ENABLE_GOOGLE_MAPS = True  # Always enabled for basic map links

# App Configuration
APP_TITLE = "Tourism Indonesia - AI Recommendations"
PAGE_ICON = "🏝️"
LAYOUT = "wide"

# Sample Data Configuration
SAMPLE_DATA_PATH = "data/sample_places.json"
DEFAULT_TOP_K = 5
MAX_PLACES_TO_EVALUATE = 50

# Indonesian Tourism Categories
TOURISM_CATEGORIES = [
    "Budaya",
    "Taman Hiburan", 
    "Cagar Alam",
    "Bahari",
    "Pusat Perbelanjaan",
    "Tempat Ibadah"
]

# Indonesian Cities
INDONESIAN_CITIES = [
    "Jakarta",
    "Bali", 
    "Yogyakarta",
    "Bandung",
    "Surabaya",
    "Medan",
    "Semarang",
    "Palembang",
    "Makassar",
    "Denpasar",
    "Malang",
    "Solo",
    "Bogor",
    "Depok",
    "Tangerang"
]

# Budget Ranges
BUDGET_RANGES = ["Low", "Medium", "High"]

# Modern UI Colors (Indonesian-inspired)
COLORS = {
    # Primary brand colors
    "primary": "#DC2626",       # Modern Indonesian Red
    "primary_light": "#FEF2F2", # Light red background
    "primary_dark": "#991B1B",   # Dark red for emphasis
    
    # Secondary colors
    "secondary": "#1F2937",      # Modern dark gray
    "secondary_light": "#F9FAFB", # Very light gray
    "secondary_dark": "#111827",  # Almost black
    
    # Accent colors
    "accent": "#F59E0B",         # Modern amber/gold
    "accent_light": "#FEF3C7",   # Light amber background
    "accent_dark": "#D97706",    # Dark amber
    
    # Success/Nature colors
    "success": "#10B981",        # Modern emerald
    "success_light": "#ECFDF5",  # Light green background
    "success_dark": "#047857",   # Dark green
    
    # Info/Ocean colors
    "info": "#3B82F6",          # Modern blue
    "info_light": "#EFF6FF",    # Light blue background
    "info_dark": "#1D4ED8",     # Dark blue
    
    # Warning colors
    "warning": "#F59E0B",       # Amber
    "warning_light": "#FFFBEB", # Light amber background
    "warning_dark": "#D97706",  # Dark amber
    
    # Error colors
    "error": "#EF4444",         # Modern red
    "error_light": "#FEF2F2",  # Light red background
    "error_dark": "#DC2626",    # Dark red
    
    # Neutral colors
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6", 
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",
    
    # Background and text
    "background": "#FFFFFF",     # Pure white
    "background_alt": "#F9FAFB", # Light gray background
    "text": "#111827",           # Almost black
    "text_light": "#6B7280",    # Light gray text
    "text_muted": "#9CA3AF",    # Muted gray text
    
    # Border colors
    "border": "#E5E7EB",        # Light border
    "border_dark": "#D1D5DB",   # Darker border
    
    # Indonesian cultural accent
    "batik": "#8B5A3C",         # Traditional brown
    "batik_light": "#F7F3F0",   # Light brown background
    
    # Aliases for backward compatibility
    "nature": "#10B981",        # Same as success - emerald green
    "ocean": "#3B82F6",         # Same as info - blue
}