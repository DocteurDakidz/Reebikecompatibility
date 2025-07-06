#!/usr/bin/env python3
"""
Reebike Kit Compatibility API
Version 1.0 - Mock implementation with local JSON data

Flask API pour évaluer la compatibilité des vélos avec les kits Reebike
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import logging
from datetime import datetime

# Configuration
app = Flask(__name__)
CORS(app)  # Enable CORS for Shopify integration

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load mock data
def load_mock_data():
    """Load mock bike data from JSON file"""
    try:
        with open('mock_bikes.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("mock_bikes.json not found, using minimal fallback data")
        return {
            "bikes": [],
            "compatibility_matrix": {
                "default_rules": {
                    "wheel_axle_front": "QR",
                    "fork_spacing_mm": 100,
                    "min_down_tube_length_mm": 300
                }
            }
        }

# Global data
mock_data = load_mock_data()

class CompatibilityAnalyzer:
    """Analyze bike compatibility with Reebike kits"""
    
    def __init__(self, data):
        self.data = data
        self.kits = {
            'Cosmopolit': {
                'requirements': {
                    'wheel_axle_front': 'QR',
                    'fork_spacing_mm': 100
                }
            },
            'Urban': {
                'requirements': {
                    'wheel_axle_front': 'QR',
                    'fork_spacing_mm': 100,
                    'min_down_tube_length_mm': 300,
                    'has_bottle_mount': True
                }
            },
            'Explorer': {
                'requirements': {
                    'wheel_axle_front': 'QR',
                    'fork_spacing_mm': 100,
                    'min_down_tube_length_mm': 350,
                    'has_bottle_mount': True
                }
            }
        }
    
    def find_bike(self, brand, model):
        """Find bike in database"""
        brand_lower = brand.lower().strip()
        model_lower = model.lower().strip()
        
        for bike in self.data.get('bikes', []):
            if (bike.get('brand', '').lower() == brand_lower and 
                model_lower in bike.get('model', '').lower()):
                return bike
        
        return None
    
    def check_compatibility(self, bike_specs):
        """Check which kits are compatible with given bike specs"""
        compatible_kits = []
        
        for kit_name, kit_info in self.kits.items():
            if self._is_kit_compatible(bike_specs, kit_info['requirements']):
                compatible_kits.append(kit_name)
        
        return compatible_kits
    
    def _is_kit_compatible(self, bike_specs, requirements):
        """Check if bike meets kit requirements"""
        for req_key, req_value in requirements.items():
            bike_value = bike_specs.get(req_key)
            
            if bike_value is None:
                return False  # Missing required data
            
            if req_key.startswith('min_') and isinstance(req_value, (int, float)):
                if bike_value < req_value:
                    return False
            elif bike_value != req_value:
                return False
        
        return True
    
    def analyze(self, brand, model):
        """Main analysis method"""
        # Find bike in database
        bike = self.find_bike(brand, model)
        
        if not bike:
            return self._handle_unknown_bike(brand, model)
        
        # Check compatibility
        compatible_kits = self.check_compatibility(bike)
        
        if not compatible_kits:
            return {
                'status': 'incompatible',
                'kits': [],
                'recommendation_url': None,
                'notes': f"Le {brand} {model} n'est pas compatible avec nos kits actuels en raison de sa géométrie spécifique."
            }
        
        # Generate recommendation URL
        primary_kit = compatible_kits[0].lower()
        recommendation_url = f"/products/kit-{primary_kit}"
        
        # Generate notes
        notes = self._generate_compatibility_notes(bike, compatible_kits)
        
        return {
            'status': 'compatible',
            'kits': compatible_kits,
            'recommendation_url': recommendation_url,
            'notes': notes
        }
    
    def _handle_unknown_bike(self, brand, model):
        """Handle unknown bike models"""
        # Check if we know the brand
        known_brands = set(bike.get('brand', '').lower() for bike in self.data.get('bikes', []))
        
        if brand.lower() in known_brands:
            notes = f"Nous connaissons la marque {brand} mais pas ce modèle spécifique ({model}). Notre équipe peut vous aider à déterminer la compatibilité."
        else:
            notes = f"Marque {brand} ou modèle {model} non reconnu dans notre base de données. Contactez notre équipe pour une analyse personnalisée."
        
        return {
            'status': 'unknown',
            'kits': [],
            'recommendation_url': None,
            'notes': notes
        }
    
    def _generate_compatibility_notes(self, bike, compatible_kits):
        """Generate helpful notes about compatibility"""
        notes = []
        
        if len(compatible_kits) == len(self.kits):
            notes.append("Excellente compatibilité ! Votre vélo est compatible avec tous nos kits.")
        elif len(compatible_kits) > 1:
            notes.append(f"Votre vélo est compatible avec {len(compatible_kits)} de nos kits.")
        else:
            notes.append("Compatibilité confirmée avec notre kit de base.")
        
        # Add specific notes based on bike characteristics
        if bike.get('has_bottle_mount'):
            notes.append("Présence d'inserts porte-gourde détectée.")
        
        if bike.get('brake_type'):
            notes.append(f"Type de freins : {bike['brake_type']}.")
        
        return " ".join(notes)

# Initialize analyzer
analyzer = CompatibilityAnalyzer(mock_data)

@app.route('/api/compat', methods=['GET'])
def check_compatibility():
    """Main compatibility check endpoint"""
    try:
        # Get parameters
        brand = request.args.get('brand', '').strip()
        model = request.args.get('model', '').strip()
        
        # Validate input
        if not brand or not model:
            return jsonify({
                'error': 'Missing required parameters',
                'message': 'Both brand and model are required'
            }), 400
        
        # Log request
        logger.info(f"Compatibility check: {brand} {model}")
        
        # Analyze compatibility
        result = analyzer.analyze(brand, model)
        
        # Log result
        logger.info(f"Result: {result['status']} - {len(result['kits'])} kits")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An error occurred while processing your request'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'bikes_count': len(mock_data.get('bikes', []))
    })

@app.route('/api/brands', methods=['GET'])
def get_brands():
    """Get list of available brands (for future autocomplete)"""
    brands = list(set(bike.get('brand', '') for bike in mock_data.get('bikes', []) if bike.get('brand')))
    brands.sort()
    
    return jsonify({
        'brands': brands,
        'count': len(brands)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)