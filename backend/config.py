#!/usr/bin/env python3
"""
Configuration settings for Reebike Compatibility API
Version 1.0
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # API settings
    API_VERSION = '1.0'
    API_TITLE = 'Reebike Compatibility API'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Rate limiting (requests per minute)
    RATE_LIMIT = int(os.environ.get('RATE_LIMIT', '60'))
    
    # Cache settings
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '300'))  # 5 minutes
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Database
    MOCK_DATA_FILE = os.environ.get('MOCK_DATA_FILE', 'mock_bikes.json')
    
    # External APIs
    GEOMETRY_GEEKS_BASE_URL = 'https://api.geometrygeeks.bike/v1'
    GEOMETRY_GEEKS_TIMEOUT = int(os.environ.get('GEOMETRY_GEEKS_TIMEOUT', '5'))
    ENABLE_GEOMETRY_GEEKS = os.environ.get('ENABLE_GEOMETRY_GEEKS', 'True').lower() == 'true'
    
    # Shopify integration
    SHOPIFY_WEBHOOK_SECRET = os.environ.get('SHOPIFY_WEBHOOK_SECRET')
    
    # Analytics
    ENABLE_ANALYTICS = os.environ.get('ENABLE_ANALYTICS', 'False').lower() == 'true'
    ANALYTICS_ENDPOINT = os.environ.get('ANALYTICS_ENDPOINT')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # Security headers
    SECURE_HEADERS = True
    
    # Rate limiting (more restrictive)
    RATE_LIMIT = 30

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    MOCK_DATA_FILE = 'test_bikes.json'
    RATE_LIMIT = 1000  # No rate limiting in tests

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])