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
                    'min_tube_length_mm': 300  # down_tube OR seat_tube
                }
            },
            'Explorer': {
                'requirements': {
                    'wheel_axle_front': 'QR',
                    'fork_spacing_mm': 100,
                    'min_tube_length_mm': 300  # down_tube OR seat_tube
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
        
        # Check basic requirements first (blocking criteria)
        if not self._meets_basic_requirements(bike_specs):
            return []
        
        # Cosmopolit is always compatible if basic requirements are met
        compatible_kits.append('Cosmopolit')
        
        # Check for Urban and Explorer compatibility
        if self._meets_advanced_requirements(bike_specs):
            compatible_kits.extend(['Urban', 'Explorer'])
        
        return compatible_kits
    
    def _meets_basic_requirements(self, bike_specs):
        """Check if bike meets basic requirements (blocking criteria)"""
        wheel_axle = bike_specs.get('wheel_axle_front')
        fork_spacing = bike_specs.get('fork_spacing_mm')
        
        # Missing critical data
        if wheel_axle is None or fork_spacing is None:
            return False
        
        # Check blocking criteria
        if wheel_axle != 'QR' or fork_spacing != 100:
            return False
        
        return True
    
    def _meets_advanced_requirements(self, bike_specs):
        """Check if bike meets advanced requirements for Urban/Explorer"""
        down_tube = bike_specs.get('down_tube_length_mm')
        seat_tube = bike_specs.get('seat_tube_length_mm')
        
        # Need at least one tube measurement
        if down_tube is None and seat_tube is None:
            return False
        
        # Check if either tube is long enough (300mm minimum)
        if down_tube is not None and down_tube >= 300:
            return True
        if seat_tube is not None and seat_tube >= 300:
            return True
        
        return False
    
    def _has_missing_data(self, bike_specs):
        """Check if bike has missing critical data"""
        required_fields = ['wheel_axle_front', 'fork_spacing_mm']
        optional_fields = ['down_tube_length_mm', 'seat_tube_length_mm']
        
        # Check required fields
        for field in required_fields:
            if bike_specs.get(field) is None:
                return True
        
        # Check if we have at least one tube measurement
        has_tube_data = any(bike_specs.get(field) is not None for field in optional_fields)
        return not has_tube_data
    
    def analyze(self, brand, model):
        """Main analysis method"""
        # Find bike in database
        bike = self.find_bike(brand, model)
        
        if not bike:
            return self._handle_unknown_bike(brand, model)
        
        # Check for missing data
        if self._has_missing_data(bike):
            return {
                'status': 'unknown',
                'kits': [],
                'recommendation_url': None,
                'notes': "Certaines données sont manquantes, contactez notre équipe."
            }
        
        # Check compatibility
        compatible_kits = self.check_compatibility(bike)
        
        if not compatible_kits:
            return {
                'status': 'incompatible',
                'kits': [],
                'recommendation_url': None,
                'notes': f"Le {brand} {model} n'est pas compatible avec nos kits actuels (axe traversant ou entraxe non standard)."
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
            notes = f"Nous connaissons la marque {brand} mais pas ce modèle spécifique ({model}). Certaines données sont manquantes, contactez notre équipe."
        else:
            notes = "Certaines données sont manquantes, contactez notre équipe."
        
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
            notes.append("Compatible si le cadre offre une longueur suffisante pour la batterie.")
        else:
            notes.append("Compatible si le cadre offre une longueur suffisante pour la batterie.")
        
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