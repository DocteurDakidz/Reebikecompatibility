#!/usr/bin/env python3
"""
Tests unitaires pour l'API de compatibilité Reebike
Version 1.0
"""

import unittest
import json
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app, analyzer

class TestCompatibilityAPI(unittest.TestCase):
    """Test cases for the compatibility API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['version'], '1.0')
        self.assertIn('timestamp', data)
    
    def test_compatibility_missing_params(self):
        """Test compatibility endpoint with missing parameters"""
        # Missing both parameters
        response = self.app.get('/api/compat')
        self.assertEqual(response.status_code, 400)
        
        # Missing model
        response = self.app.get('/api/compat?brand=Trek')
        self.assertEqual(response.status_code, 400)
        
        # Missing brand
        response = self.app.get('/api/compat?model=Domane')
        self.assertEqual(response.status_code, 400)
    
    def test_compatibility_known_bike_compatible(self):
        """Test compatibility with known compatible bike"""
        response = self.app.get('/api/compat?brand=Trek&model=Domane SL 2023')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'compatible')
        self.assertIsInstance(data['kits'], list)
        self.assertGreater(len(data['kits']), 0)
        self.assertIsNotNone(data['recommendation_url'])
    
    def test_compatibility_known_bike_incompatible(self):
        """Test compatibility with known incompatible bike"""
        response = self.app.get('/api/compat?brand=Trek&model=Madone SLR 2023')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'incompatible')
        self.assertEqual(len(data['kits']), 0)
        self.assertIsNone(data['recommendation_url'])
    
    def test_compatibility_unknown_bike(self):
        """Test compatibility with unknown bike"""
        response = self.app.get('/api/compat?brand=UnknownBrand&model=UnknownModel')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'unknown')
        self.assertEqual(len(data['kits']), 0)
        self.assertIsNone(data['recommendation_url'])
        self.assertIn('notes', data)
    
    def test_brands_endpoint(self):
        """Test brands listing endpoint"""
        response = self.app.get('/api/brands')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('brands', data)
        self.assertIn('count', data)
        self.assertIsInstance(data['brands'], list)
        self.assertGreater(data['count'], 0)
    
    def test_404_endpoint(self):
        """Test 404 handling"""
        response = self.app.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not found')

class TestCompatibilityAnalyzer(unittest.TestCase):
    """Test cases for the compatibility analyzer logic"""
    
    def test_find_bike_exact_match(self):
        """Test finding bike with exact match"""
        bike = analyzer.find_bike('Trek', 'Domane SL 2023')
        self.assertIsNotNone(bike)
        self.assertEqual(bike['brand'], 'Trek')
        self.assertIn('Domane', bike['model'])
    
    def test_find_bike_case_insensitive(self):
        """Test finding bike with case insensitive search"""
        bike = analyzer.find_bike('trek', 'domane sl 2023')
        self.assertIsNotNone(bike)
        self.assertEqual(bike['brand'], 'Trek')
    
    def test_find_bike_not_found(self):
        """Test finding non-existent bike"""
        bike = analyzer.find_bike('NonExistent', 'Model')
        self.assertIsNone(bike)
    
    def test_compatibility_check_cosmopolit(self):
        """Test Cosmopolit kit compatibility"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            'fork_spacing_mm': 100,
            'down_tube_length_mm': 250,  # Too short for Urban/Explorer
            'seat_tube_length_mm': 280   # Also too short
        }
        
        compatible_kits = analyzer.check_compatibility(bike_specs)
        self.assertIn('Cosmopolit', compatible_kits)
        self.assertNotIn('Urban', compatible_kits)
        self.assertNotIn('Explorer', compatible_kits)
    
    def test_compatibility_check_all_kits(self):
        """Test compatibility with all kits"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            'fork_spacing_mm': 100,
            'down_tube_length_mm': 360,
            'seat_tube_length_mm': 380
        }
        
        compatible_kits = analyzer.check_compatibility(bike_specs)
        self.assertIn('Cosmopolit', compatible_kits)
        self.assertIn('Urban', compatible_kits)
        self.assertIn('Explorer', compatible_kits)
    
    def test_compatibility_check_seat_tube_only(self):
        """Test compatibility with only seat tube measurement"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            'fork_spacing_mm': 100,
            'seat_tube_length_mm': 320  # Sufficient for Urban/Explorer
        }
        
        compatible_kits = analyzer.check_compatibility(bike_specs)
        self.assertIn('Cosmopolit', compatible_kits)
        self.assertIn('Urban', compatible_kits)
        self.assertIn('Explorer', compatible_kits)
    
    def test_compatibility_check_incompatible(self):
        """Test incompatible bike specs"""
        bike_specs = {
            'wheel_axle_front': 'Thru-axle',  # Incompatible
            'fork_spacing_mm': 100,
            'down_tube_length_mm': 350,
            'seat_tube_length_mm': 380
        }
        
        compatible_kits = analyzer.check_compatibility(bike_specs)
        self.assertEqual(len(compatible_kits), 0)
    
    def test_missing_data_unknown_status(self):
        """Test unknown status when data is missing"""
        result = analyzer.analyze('Trek', 'Unknown Model')
        self.assertEqual(result['status'], 'unknown')
        self.assertEqual(result['notes'], 'Certaines données sont manquantes, contactez notre équipe.')

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)