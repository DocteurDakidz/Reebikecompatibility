#!/usr/bin/env python3
"""
Utility functions for Reebike Compatibility API
Version 1.0
"""

import json
import logging
import re
from datetime import datetime
from functools import wraps
from flask import request, jsonify

logger = logging.getLogger(__name__)

def validate_bike_input(brand, model):
    """
    Validate bike brand and model input
    
    Args:
        brand (str): Bike brand
        model (str): Bike model
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not brand or not isinstance(brand, str):
        return False, "Brand is required and must be a string"
    
    if not model or not isinstance(model, str):
        return False, "Model is required and must be a string"
    
    # Check length limits
    if len(brand) > 50:
        return False, "Brand name too long (max 50 characters)"
    
    if len(model) > 100:
        return False, "Model name too long (max 100 characters)"
    
    # Check for valid characters (letters, numbers, spaces, hyphens)
    valid_pattern = re.compile(r'^[a-zA-Z0-9\s\-\.]+$')
    
    if not valid_pattern.match(brand):
        return False, "Brand contains invalid characters"
    
    if not valid_pattern.match(model):
        return False, "Model contains invalid characters"
    
    return True, None

def normalize_bike_name(name):
    """
    Normalize bike brand/model name for comparison
    
    Args:
        name (str): Brand or model name
        
    Returns:
        str: Normalized name
    """
    if not name:
        return ""
    
    # Convert to lowercase and strip whitespace
    normalized = name.lower().strip()
    
    # Remove extra spaces
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Remove common suffixes/prefixes that might vary
    suffixes_to_remove = [
        r'\s+\d{4}$',  # Year (e.g., "2023")
        r'\s+bike$',   # "bike"
        r'\s+bicycle$' # "bicycle"
    ]
    
    for suffix in suffixes_to_remove:
        normalized = re.sub(suffix, '', normalized)
    
    return normalized

def log_compatibility_request(brand, model, result):
    """
    Log compatibility request for analytics
    
    Args:
        brand (str): Bike brand
        model (str): Bike model
        result (dict): Compatibility result
    """
    try:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'brand': brand,
            'model': model,
            'status': result.get('status'),
            'kits_count': len(result.get('kits', [])),
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')[:100]
        }
        
        logger.info(f"Compatibility request: {json.dumps(log_entry)}")
        
    except Exception as e:
        logger.error(f"Failed to log compatibility request: {str(e)}")

def rate_limit_key():
    """
    Generate rate limit key based on IP address
    
    Returns:
        str: Rate limit key
    """
    return f"rate_limit:{request.remote_addr}"

def handle_api_error(func):
    """
    Decorator to handle API errors consistently
    
    Args:
        func: Function to wrap
        
    Returns:
        function: Wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            return jsonify({
                'error': 'Validation error',
                'message': str(e)
            }), 400
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred'
            }), 500
    
    return wrapper

def format_compatibility_response(status, kits, recommendation_url, notes):
    """
    Format compatibility response consistently
    
    Args:
        status (str): Compatibility status
        kits (list): Compatible kits
        recommendation_url (str): Recommendation URL
        notes (str): Additional notes
        
    Returns:
        dict: Formatted response
    """
    return {
        'status': status,
        'kits': kits or [],
        'recommendation_url': recommendation_url,
        'notes': notes or '',
        'timestamp': datetime.now().isoformat(),
        'api_version': '1.0'
    }

def load_json_file(filepath, default=None):
    """
    Safely load JSON file with error handling
    
    Args:
        filepath (str): Path to JSON file
        default: Default value if file not found
        
    Returns:
        dict: Loaded JSON data or default
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"JSON file not found: {filepath}")
        return default or {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {filepath}: {str(e)}")
        return default or {}
    except Exception as e:
        logger.error(f"Error loading JSON file {filepath}: {str(e)}")
        return default or {}

def sanitize_input(text, max_length=100):
    """
    Sanitize user input
    
    Args:
        text (str): Input text
        max_length (int): Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Strip whitespace and limit length
    sanitized = text.strip()[:max_length]
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\']', '', sanitized)
    
    return sanitized

def generate_recommendation_url(kit_name):
    """
    Generate product recommendation URL
    
    Args:
        kit_name (str): Name of the kit
        
    Returns:
        str: Product URL
    """
    if not kit_name:
        return None
    
    # Convert kit name to URL-friendly format
    url_name = kit_name.lower().replace(' ', '-')
    return f"/products/kit-{url_name}"

def calculate_compatibility_score(bike_specs, kit_requirements):
    """
    Calculate compatibility score between bike and kit
    
    Args:
        bike_specs (dict): Bike specifications
        kit_requirements (dict): Kit requirements
        
    Returns:
        float: Compatibility score (0.0 to 1.0)
    """
    if not bike_specs or not kit_requirements:
        return 0.0
    
    total_requirements = len(kit_requirements)
    met_requirements = 0
    
    for req_key, req_value in kit_requirements.items():
        bike_value = bike_specs.get(req_key)
        
        if bike_value is None:
            continue
        
        if req_key.startswith('min_') and isinstance(req_value, (int, float)):
            if bike_value >= req_value:
                met_requirements += 1
        elif bike_value == req_value:
            met_requirements += 1
    
    return met_requirements / total_requirements if total_requirements > 0 else 0.0