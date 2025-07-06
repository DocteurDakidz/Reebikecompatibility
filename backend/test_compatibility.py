import pytest
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_functionality():
    """Basic test to ensure the test framework is working"""
    assert True

def test_backend_directory_exists():
    """Test that we're in the correct directory structure"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assert os.path.basename(current_dir) == 'backend'

if __name__ == "__main__":
    pytest.main([__file__])