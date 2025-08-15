"""
Input validation utilities for tourism frontend
"""

import streamlit as st
from typing import Dict, Any, List, Optional, Tuple
from config import TOURISM_CATEGORIES, INDONESIAN_CITIES, BUDGET_RANGES

def validate_age(age: int) -> Tuple[bool, str]:
    """Validate user age input."""
    if not isinstance(age, int):
        return False, "Age must be a number"
    
    if age < 18:
        return False, "Age must be at least 18"
    
    if age > 100:
        return False, "Age must be at most 100"
    
    return True, ""

def validate_category(category: Optional[str]) -> Tuple[bool, str]:
    """Validate tourism category selection."""
    if category is None or category == "All":
        return True, ""
    
    if category not in TOURISM_CATEGORIES:
        return False, f"Invalid category. Must be one of: {', '.join(TOURISM_CATEGORIES)}"
    
    return True, ""

def validate_city(city: Optional[str]) -> Tuple[bool, str]:
    """Validate city selection."""
    if city is None or city == "All":
        return True, ""
    
    if city not in INDONESIAN_CITIES:
        return False, f"Invalid city. Must be one of: {', '.join(INDONESIAN_CITIES)}"
    
    return True, ""

def validate_budget_range(budget: Optional[str]) -> Tuple[bool, str]:
    """Validate budget range selection."""
    if budget is None:
        return False, "Budget range is required"
    
    if budget not in BUDGET_RANGES:
        return False, f"Invalid budget range. Must be one of: {', '.join(BUDGET_RANGES)}"
    
    return True, ""

def validate_price(price: float) -> Tuple[bool, str]:
    """Validate price input."""
    if not isinstance(price, (int, float)):
        return False, "Price must be a number"
    
    if price < 0:
        return False, "Price cannot be negative"
    
    if price > 10000000:  # 10 million IDR
        return False, "Price seems unrealistically high (max 10M IDR)"
    
    return True, ""

def validate_rating(rating: float) -> Tuple[bool, str]:
    """Validate rating input."""
    if not isinstance(rating, (int, float)):
        return False, "Rating must be a number"
    
    if rating < 1.0:
        return False, "Rating must be at least 1.0"
    
    if rating > 5.0:
        return False, "Rating must be at most 5.0"
    
    return True, ""

def validate_top_k(top_k: int) -> Tuple[bool, str]:
    """Validate top-k recommendations count."""
    if not isinstance(top_k, int):
        return False, "Number of recommendations must be an integer"
    
    if top_k < 1:
        return False, "Must request at least 1 recommendation"
    
    if top_k > 20:
        return False, "Cannot request more than 20 recommendations"
    
    return True, ""

def validate_user_preferences(preferences: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate all user preferences and return validation errors."""
    errors = {}
    
    # Validate age
    if 'user_age' in preferences:
        is_valid, error = validate_age(preferences['user_age'])
        if not is_valid:
            errors['user_age'] = [error]
    
    # Validate category
    if 'preferred_category' in preferences:
        is_valid, error = validate_category(preferences['preferred_category'])
        if not is_valid:
            errors['preferred_category'] = [error]
    
    # Validate city
    if 'preferred_city' in preferences:
        is_valid, error = validate_city(preferences['preferred_city'])
        if not is_valid:
            errors['preferred_city'] = [error]
    
    # Validate budget range
    if 'budget_range' in preferences:
        is_valid, error = validate_budget_range(preferences['budget_range'])
        if not is_valid:
            errors['budget_range'] = [error]
    
    # Validate max price
    if 'max_price' in preferences:
        is_valid, error = validate_price(preferences['max_price'])
        if not is_valid:
            errors['max_price'] = [error]
    
    # Validate min rating
    if 'min_rating' in preferences:
        is_valid, error = validate_rating(preferences['min_rating'])
        if not is_valid:
            errors['min_rating'] = [error]
    
    # Validate top_k
    if 'top_k' in preferences:
        is_valid, error = validate_top_k(preferences['top_k'])
        if not is_valid:
            errors['top_k'] = [error]
    
    return errors

def validate_place_data(place: Dict[str, Any]) -> Dict[str, List[str]]:
    """Validate place data structure."""
    errors = {}
    required_fields = [
        'place_id', 'place_category', 'place_city', 
        'place_price', 'place_average_rating', 'place_visit_duration_minutes'
    ]
    
    # Check required fields
    for field in required_fields:
        if field not in place:
            if 'structure' not in errors:
                errors['structure'] = []
            errors['structure'].append(f"Missing required field: {field}")
    
    # Validate specific fields if present
    if 'place_price' in place:
        is_valid, error = validate_price(place['place_price'])
        if not is_valid:
            errors['place_price'] = [error]
    
    if 'place_average_rating' in place:
        is_valid, error = validate_rating(place['place_average_rating'])
        if not is_valid:
            errors['place_average_rating'] = [error]
    
    if 'place_visit_duration_minutes' in place:
        if not isinstance(place['place_visit_duration_minutes'], int) or place['place_visit_duration_minutes'] < 1:
            errors['place_visit_duration_minutes'] = ["Duration must be a positive integer"]
    
    if 'place_category' in place:
        is_valid, error = validate_category(place['place_category'])
        if not is_valid:
            errors['place_category'] = [error]
    
    if 'place_city' in place:
        is_valid, error = validate_city(place['place_city'])
        if not is_valid:
            errors['place_city'] = [error]
    
    return errors

def display_validation_errors(errors: Dict[str, List[str]], title: str = "Validation Errors") -> None:
    """Display validation errors in Streamlit UI."""
    if not errors:
        return
    
    st.error(f"**{title}**")
    
    for field, field_errors in errors.items():
        for error in field_errors:
            st.error(f"• **{field}**: {error}")

def sanitize_user_input(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize and clean user input preferences."""
    sanitized = {}
    
    # Age: ensure integer in valid range
    if 'user_age' in preferences:
        try:
            age = int(preferences['user_age'])
            sanitized['user_age'] = max(18, min(100, age))
        except (ValueError, TypeError):
            sanitized['user_age'] = 25  # Default age
    
    # Category: ensure valid or None
    if 'preferred_category' in preferences:
        category = preferences['preferred_category']
        if category == "All" or category not in TOURISM_CATEGORIES:
            sanitized['preferred_category'] = None
        else:
            sanitized['preferred_category'] = category
    
    # City: ensure valid or None
    if 'preferred_city' in preferences:
        city = preferences['preferred_city']
        if city == "All" or city not in INDONESIAN_CITIES:
            sanitized['preferred_city'] = None
        else:
            sanitized['preferred_city'] = city
    
    # Budget range: ensure valid
    if 'budget_range' in preferences:
        budget = preferences['budget_range']
        if budget not in BUDGET_RANGES:
            sanitized['budget_range'] = "Medium"  # Default
        else:
            sanitized['budget_range'] = budget
    
    # Max price: ensure positive number
    if 'max_price' in preferences:
        try:
            price = float(preferences['max_price'])
            sanitized['max_price'] = max(0, min(10000000, price))
        except (ValueError, TypeError):
            sanitized['max_price'] = 200000  # Default
    
    # Min rating: ensure valid range
    if 'min_rating' in preferences:
        try:
            rating = float(preferences['min_rating'])
            sanitized['min_rating'] = max(1.0, min(5.0, rating))
        except (ValueError, TypeError):
            sanitized['min_rating'] = 3.0  # Default
    
    # Top K: ensure valid integer
    if 'top_k' in preferences:
        try:
            top_k = int(preferences['top_k'])
            sanitized['top_k'] = max(1, min(20, top_k))
        except (ValueError, TypeError):
            sanitized['top_k'] = 5  # Default
    
    return sanitized

@st.cache_data
def get_validation_schema() -> Dict[str, Dict[str, Any]]:
    """Get validation schema for API documentation."""
    return {
        'user_preferences': {
            'user_age': {'type': 'integer', 'minimum': 18, 'maximum': 100, 'required': True},
            'preferred_category': {'type': 'string', 'enum': TOURISM_CATEGORIES + [None], 'required': False},
            'preferred_city': {'type': 'string', 'enum': INDONESIAN_CITIES + [None], 'required': False},
            'budget_range': {'type': 'string', 'enum': BUDGET_RANGES, 'required': True},
            'max_price': {'type': 'number', 'minimum': 0, 'maximum': 10000000, 'required': False},
            'min_rating': {'type': 'number', 'minimum': 1.0, 'maximum': 5.0, 'required': False},
            'top_k': {'type': 'integer', 'minimum': 1, 'maximum': 20, 'required': False}
        },
        'place_data': {
            'place_id': {'type': 'string', 'required': True},
            'place_category': {'type': 'string', 'enum': TOURISM_CATEGORIES, 'required': True},
            'place_city': {'type': 'string', 'enum': INDONESIAN_CITIES, 'required': True},
            'place_price': {'type': 'number', 'minimum': 0, 'required': True},
            'place_average_rating': {'type': 'number', 'minimum': 1.0, 'maximum': 5.0, 'required': True},
            'place_visit_duration_minutes': {'type': 'integer', 'minimum': 1, 'required': True},
            'place_description': {'type': 'string', 'required': False}
        }
    }