#!/usr/bin/env python3
"""
Tests unitaires pour l'API de compatibilité Reebike
Version 1.0 - Tests complets
"""

import unittest
import json
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, analyzer, CompatibilityAnalyzer

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
        self.assertIn('bikes_count', data)
    
    def test_compatibility_missing_params(self):
        """Test compatibility endpoint with missing parameters"""
        # Missing both parameters
        response = self.app.get('/api/compat')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Missing required parameters')
        
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
        self.assertIn('notes', data)
    
    def test_compatibility_known_bike_incompatible(self):
        """Test compatibility with known incompatible bike"""
        response = self.app.get('/api/compat?brand=Trek&model=Madone SLR 2023')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'incompatible')
        self.assertEqual(len(data['kits']), 0)
        self.assertIsNone(data['recommendation_url'])
        self.assertIn('notes', data)
    
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
        
        # Check that brands are sorted
        brands = data['brands']
        self.assertEqual(brands, sorted(brands))
    
    def test_404_endpoint(self):
        """Test 404 handling"""
        response = self.app.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not found')
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = self.app.get('/api/health')
        self.assertIn('Access-Control-Allow-Origin', response.headers)

class TestCompatibilityAnalyzer(unittest.TestCase):
    """Test cases for the compatibility analyzer logic"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = {
            "bikes": [
                {
                    "brand": "TestBrand",
                    "model": "TestModel Compatible",
                    "wheel_axle_front": "QR",
                    "fork_spacing_mm": 100,
                    "down_tube_length_mm": 350,
                    "has_bottle_mount": True,
                    "brake_type": "Rim"
                },
                {
                    "brand": "TestBrand",
                    "model": "TestModel Incompatible",
                    "wheel_axle_front": "Thru-axle",
                    "fork_spacing_mm": 100,
                    "down_tube_length_mm": 350,
                    "has_bottle_mount": True,
                    "brake_type": "Disc"
                }
            ]
        }
        self.analyzer = CompatibilityAnalyzer(self.test_data)
    
    def test_find_bike_exact_match(self):
        """Test finding bike with exact match"""
        bike = self.analyzer.find_bike('TestBrand', 'TestModel Compatible')
        self.assertIsNotNone(bike)
        self.assertEqual(bike['brand'], 'TestBrand')
        self.assertIn('Compatible', bike['model'])
    
    def test_find_bike_case_insensitive(self):
        """Test finding bike with case insensitive search"""
        bike = self.analyzer.find_bike('testbrand', 'testmodel compatible')
        self.assertIsNotNone(bike)
        self.assertEqual(bike['brand'], 'TestBrand')
    
    def test_find_bike_partial_model_match(self):
        """Test finding bike with partial model match"""
        bike = self.analyzer.find_bike('TestBrand', 'Compatible')
        self.assertIsNotNone(bike)
        self.assertEqual(bike['brand'], 'TestBrand')
    
    def test_find_bike_not_found(self):
        """Test finding non-existent bike"""
        bike = self.analyzer.find_bike('NonExistent', 'Model')
        self.assertIsNone(bike)
    
    def test_compatibility_check_cosmopolit_only(self):
        """Test Cosmopolit kit compatibility only"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            'fork_spacing_mm': 100,
            'down_tube_length_mm': 250,  # Too short for Urban/Explorer
            'has_bottle_mount': False
        }
        
        compatible_kits = self.analyzer.check_compatibility(bike_specs)
        self.assertIn('Cosmopolit', compatible_kits)
        self.assertNotIn('Urban', compatible_kits)
        self.assertNotIn('Explorer', compatible_kits)
    
    def test_compatibility_check_urban_compatible(self):
        """Test Urban kit compatibility"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            'fork_spacing_mm': 100,
            'down_tube_length_mm': 320,
            'has_bottle_mount': True
        }
        
        compatible_kits = self.analyzer.check_compatibility(bike_specs)
        self.assertIn('Cosmopolit', compatible_kits)
        self.assertIn('Urban', compatible_kits)
        self.assertNotIn('Explorer', compatible_kits)  # Needs 350mm
    
    def test_compatibility_check_all_kits(self):
        """Test compatibility with all kits"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            'fork_spacing_mm': 100,
            'down_tube_length_mm': 360,
            'has_bottle_mount': True
        }
        
        compatible_kits = self.analyzer.check_compatibility(bike_specs)
        self.assertIn('Cosmopolit', compatible_kits)
        self.assertIn('Urban', compatible_kits)
        self.assertIn('Explorer', compatible_kits)
    
    def test_compatibility_check_incompatible_axle(self):
        """Test incompatible bike specs - wrong axle"""
        bike_specs = {
            'wheel_axle_front': 'Thru-axle',  # Incompatible
            'fork_spacing_mm': 100,
            'down_tube_length_mm': 350,
            'has_bottle_mount': True
        }
        
        compatible_kits = self.analyzer.check_compatibility(bike_specs)
        self.assertEqual(len(compatible_kits), 0)
    
    def test_compatibility_check_incompatible_spacing(self):
        """Test incompatible bike specs - wrong fork spacing"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            'fork_spacing_mm': 130,  # Incompatible
            'down_tube_length_mm': 350,
            'has_bottle_mount': True
        }
        
        compatible_kits = self.analyzer.check_compatibility(bike_specs)
        self.assertEqual(len(compatible_kits), 0)
    
    def test_compatibility_check_missing_data(self):
        """Test compatibility check with missing data"""
        bike_specs = {
            'wheel_axle_front': 'QR',
            # Missing fork_spacing_mm
            'down_tube_length_mm': 350,
            'has_bottle_mount': True
        }
        
        compatible_kits = self.analyzer.check_compatibility(bike_specs)
        self.assertEqual(len(compatible_kits), 0)
    
    def test_analyze_compatible_bike(self):
        """Test full analysis of compatible bike"""
        result = self.analyzer.analyze('TestBrand', 'TestModel Compatible')
        
        self.assertEqual(result['status'], 'compatible')
        self.assertGreater(len(result['kits']), 0)
        self.assertIsNotNone(result['recommendation_url'])
        self.assertIn('notes', result)
    
    def test_analyze_incompatible_bike(self):
        """Test full analysis of incompatible bike"""
        result = self.analyzer.analyze('TestBrand', 'TestModel Incompatible')
        
        self.assertEqual(result['status'], 'incompatible')
        self.assertEqual(len(result['kits']), 0)
        self.assertIsNone(result['recommendation_url'])
        self.assertIn('notes', result)
    
    def test_analyze_unknown_bike(self):
        """Test full analysis of unknown bike"""
        result = self.analyzer.analyze('UnknownBrand', 'UnknownModel')
        
        self.assertEqual(result['status'], 'unknown')
        self.assertEqual(len(result['kits']), 0)
        self.assertIsNone(result['recommendation_url'])
        self.assertIn('notes', result)
    
    def test_generate_compatibility_notes(self):
        """Test compatibility notes generation"""
        bike = self.test_data['bikes'][0]  # Compatible bike
        compatible_kits = ['Cosmopolit', 'Urban', 'Explorer']
        
        notes = self.analyzer._generate_compatibility_notes(bike, compatible_kits)
        
        self.assertIn('tous nos kits', notes)
        self.assertIn('porte-gourde', notes)
        self.assertIn('Rim', notes)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)