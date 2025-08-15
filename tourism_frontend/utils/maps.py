"""
Google Maps integration utilities
"""

import urllib.parse
from typing import Dict, Any, Optional, Tuple
from config import ENABLE_GOOGLE_MAPS

# Coordinates for major Indonesian tourist destinations
PLACE_COORDINATES = {
    # Yogyakarta area
    "borobudur_001": (-7.6079, 110.2038),
    "gembira_loka_003": (-7.7828, 110.4025),
    "malioboro_010": (-7.7938, 110.3656),
    
    # Bali area
    "uluwatu_002": (-8.8297, 115.0843),
    "kuta_beach_007": (-8.7192, 115.1686),
    
    # Jakarta area
    "ancol_004": (-6.1268, 106.8347),
    "grand_indonesia_009": (-6.1944, 106.8229),
    "istiqlal_011": (-6.1702, 106.8314),
    
    # East Java area
    "komodo_005": (-8.5594, 119.6895), # Komodo National Park
    "bromo_006": (-7.9425, 112.9530),
    
    # Lombok area  
    "gili_islands_008": (-8.3484, 116.0289),
    
    # Additional coordinates for common places
    "prambanan_012": (-7.7520, 110.4915),
    "tanah_lot_013": (-8.6214, 115.0868),
    "mount_batur_014": (-8.2422, 115.3755),
    "sekumpul_015": (-8.1539, 115.1539),
    "nusa_penida_016": (-8.7286, 115.5442),
    "kelingking_017": (-8.7642, 115.4389),
    "taman_sari_018": (-7.8059, 110.3587),
    "keraton_019": (-7.8052, 110.3642),
    "lawang_sewu_020": (-6.9667, 110.4167),
    "simpang_lima_021": (-6.9667, 110.4167),
    "sam_poo_kong_022": (-6.9895, 110.4108),
    "brown_canyon_023": (-6.9000, 110.5000),
    "umbul_ponggok_024": (-7.6500, 110.6000),
    "jomblang_cave_025": (-7.9000, 110.6500),
    "timang_beach_026": (-8.1444, 110.6072),
    "indrayanti_beach_027": (-8.1500, 110.6000),
    "parangtritis_028": (-8.0250, 110.3294),
    "sultan_palace_029": (-7.8052, 110.3642),
    "silver_beach_030": (-8.1667, 110.5833),
}

def get_place_coordinates(place_id: str) -> Optional[Tuple[float, float]]:
    """Get coordinates for a place by its ID."""
    return PLACE_COORDINATES.get(place_id)

def generate_google_maps_url(place_name: str, coordinates: Optional[Tuple[float, float]] = None, 
                           place_id: str = None) -> str:
    """
    Generate Google Maps URL for a place.
    
    Args:
        place_name: Name of the place
        coordinates: Optional (latitude, longitude) tuple
        place_id: Optional place ID to lookup coordinates
    
    Returns:
        Google Maps URL
    """
    # Try to get coordinates from place_id if not provided
    if coordinates is None and place_id:
        coordinates = get_place_coordinates(place_id)
    
    # If we have coordinates, use them for precise location
    if coordinates:
        lat, lng = coordinates
        base_url = "https://www.google.com/maps"
        params = {
            'q': f"{lat},{lng}({place_name})",
            'z': '15'  # Zoom level
        }
        return f"{base_url}?{urllib.parse.urlencode(params)}"
    
    # Fallback to search by name
    base_url = "https://www.google.com/maps/search/"
    encoded_name = urllib.parse.quote(place_name)
    return f"{base_url}{encoded_name}"

# Removed embed URL function - not needed for basic maps integration

def generate_directions_url(destination: str, coordinates: Optional[Tuple[float, float]] = None,
                          place_id: str = None) -> str:
    """
    Generate Google Maps directions URL.
    
    Args:
        destination: Destination name
        coordinates: Optional (latitude, longitude) tuple
        place_id: Optional place ID to lookup coordinates
    
    Returns:
        Google Maps directions URL
    """
    # Try to get coordinates from place_id if not provided
    if coordinates is None and place_id:
        coordinates = get_place_coordinates(place_id)
    
    base_url = "https://www.google.com/maps/dir/"
    
    if coordinates:
        lat, lng = coordinates
        # Format: /current+location/lat,lng
        return f"{base_url}current+location/{lat},{lng}"
    
    # Fallback to destination name
    encoded_destination = urllib.parse.quote(destination)
    return f"{base_url}current+location/{encoded_destination}"

def format_place_name_for_maps(place: Dict[str, Any]) -> str:
    """
    Format place name for Google Maps search.
    
    Args:
        place: Place data dictionary
    
    Returns:
        Formatted place name
    """
    place_name = place['place_id'].replace('_', ' ').title()
    city = place['place_city']
    
    # Add city and country for better search results
    return f"{place_name}, {city}, Indonesia"

def get_place_maps_data(place: Dict[str, Any]) -> Dict[str, str]:
    """
    Get all Google Maps URLs for a place.
    
    Args:
        place: Place data dictionary
    
    Returns:
        Dictionary with different Google Maps URLs
    """
    place_id = place['place_id']
    coordinates = get_place_coordinates(place_id)
    formatted_name = format_place_name_for_maps(place)
    
    return {
        'view_url': generate_google_maps_url(formatted_name, coordinates, place_id),
        'directions_url': generate_directions_url(formatted_name, coordinates, place_id),
        'coordinates': coordinates,
        'formatted_name': formatted_name
    }