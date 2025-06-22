import requests
import json
import time
import urllib.parse
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint returns welcome message and endpoint list."""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    print("✅ Root endpoint test passed")

def test_timezones_endpoint():
    """Test the timezones endpoint returns list of all timezones."""
    print("Testing timezones endpoint...")
    response = requests.get(f"{BASE_URL}/timezones")
    assert response.status_code == 200
    data = response.json()
    assert "timezones" in data
    assert isinstance(data["timezones"], list)
    assert len(data["timezones"]) > 0
    print("✅ Timezones endpoint test passed")

def test_search_endpoint():
    """Test the search endpoint with various search terms."""
    print("Testing search endpoint...")
    
    # Test basic search
    response = requests.get(f"{BASE_URL}/timezones/search?q=America")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "count" in data
    assert "search_term" in data
    assert data["search_term"] == "America"
    
    # Test search with no results
    response = requests.get(f"{BASE_URL}/timezones/search?q=InvalidTimezone123")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    
    print("✅ Search endpoint test passed")

def test_current_time_single():
    """Test getting current time for a single timezone."""
    print("Testing current time single endpoint...")
    
    # Test with URL encoding
    timezone = "America/New_York"
    encoded_timezone = urllib.parse.quote(timezone)
    response = requests.get(f"{BASE_URL}/current/{encoded_timezone}")
    
    if response.status_code != 200:
        print(f"❌ Current time single test failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    data = response.json()
    assert "current_time" in data
    assert "timezone" in data
    assert "utc_offset" in data
    assert "is_dst" in data
    assert data["timezone"] == timezone
    print("✅ Current time single test passed")
    return True

def test_current_time_multiple():
    """Test getting current time for multiple timezones."""
    print("Testing current time multiple endpoint...")
    response = requests.get(f"{BASE_URL}/current?timezones=UTC,America/New_York,Europe/London")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 3
    
    # Check each result has required fields
    for result in data["results"]:
        assert "timezone" in result
        assert "current_time" in result
        assert "utc_offset" in result
        assert "is_dst" in result
    
    print("✅ Current time multiple test passed")

def test_timezone_info():
    """Test getting detailed timezone information."""
    print("Testing timezone info endpoint...")
    
    # Test with URL encoding
    timezone = "America/New_York"
    encoded_timezone = urllib.parse.quote(timezone)
    response = requests.get(f"{BASE_URL}/info/{encoded_timezone}")
    
    if response.status_code != 200:
        print(f"❌ Timezone info test failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    data = response.json()
    assert "timezone" in data
    assert "current_time" in data
    assert "utc_offset" in data
    assert "is_dst" in data
    assert "dst_name" in data
    assert data["timezone"] == timezone
    print("✅ Timezone info test passed")
    return True

def test_single_conversion():
    """Test single time conversion."""
    print("Testing single conversion endpoint...")
    payload = {
        "datetime": "2023-12-25 12:00:00",
        "source_timezone": "UTC",
        "target_timezone": "America/New_York"
    }
    response = requests.post(f"{BASE_URL}/convert", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "source_time" in data
    assert "source_timezone" in data
    assert "converted_time" in data
    assert "target_timezone" in data
    assert data["source_timezone"] == "UTC"
    assert data["target_timezone"] == "America/New_York"
    print("✅ Single conversion test passed")

def test_batch_conversion():
    """Test batch time conversion."""
    print("Testing batch conversion endpoint...")
    payload = {
        "conversions": [
            {
                "datetime": "2023-12-25 12:00:00",
                "source_timezone": "UTC",
                "target_timezone": "America/New_York"
            },
            {
                "datetime": "2023-12-25 15:00:00",
                "source_timezone": "UTC",
                "target_timezone": "Europe/London"
            },
            {
                "datetime": "2023-12-25 18:00:00",
                "source_timezone": "UTC",
                "target_timezone": "Asia/Tokyo"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/convert/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 3
    
    # Check each result
    for result in data["results"]:
        assert "source_time" in result
        assert "source_timezone" in result
        assert "converted_time" in result
        assert "target_timezone" in result
    
    print("✅ Batch conversion test passed")

def test_error_handling():
    """Test various error scenarios."""
    print("Testing error handling...")
    
    # Test invalid timezone in current time
    response = requests.get(f"{BASE_URL}/current/Invalid/Timezone")
    assert response.status_code == 400
    
    # Test invalid timezone in info
    response = requests.get(f"{BASE_URL}/info/Invalid/Timezone")
    assert response.status_code == 400
    
    # Test invalid conversion
    payload = {
        "datetime": "invalid-datetime",
        "source_timezone": "UTC",
        "target_timezone": "America/New_York"
    }
    response = requests.post(f"{BASE_URL}/convert", json=payload)
    assert response.status_code == 400
    
    # Test invalid source timezone
    payload = {
        "datetime": "2023-12-25 12:00:00",
        "source_timezone": "Invalid/Timezone",
        "target_timezone": "America/New_York"
    }
    response = requests.post(f"{BASE_URL}/convert", json=payload)
    assert response.status_code == 400
    
    print("✅ Error handling test passed")

def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("Testing edge cases...")
    
    # Test UTC timezone
    response = requests.get(f"{BASE_URL}/current/UTC")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "UTC"
    
    # Test conversion with same source and target
    payload = {
        "datetime": "2023-12-25 12:00:00",
        "source_timezone": "UTC",
        "target_timezone": "UTC"
    }
    response = requests.post(f"{BASE_URL}/convert", json=payload)
    assert response.status_code == 200
    
    print("✅ Edge cases test passed")

def test_performance():
    """Test API performance with multiple requests."""
    print("Testing performance...")
    
    start_time = time.time()
    
    # Make 10 requests to test performance
    for i in range(10):
        response = requests.get(f"{BASE_URL}/timezones")
        assert response.status_code == 200
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / 10
    
    print(f"✅ Performance test passed - Average response time: {avg_time:.3f}s")

def test_api_documentation():
    """Test that API documentation is accessible."""
    print("Testing API documentation...")
    
    # Test OpenAPI docs
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200
    
    # Test OpenAPI JSON
    response = requests.get(f"{BASE_URL}/openapi.json")
    assert response.status_code == 200
    
    print("✅ API documentation test passed")

def run_all_tests():
    """Run all tests and provide summary."""
    print("🧪 Starting Time Zone Converter API Tests...")
    print("=" * 50)
    
    tests = [
        test_root_endpoint,
        test_timezones_endpoint,
        test_search_endpoint,
        test_current_time_single,
        test_current_time_multiple,
        test_timezone_info,
        test_single_conversion,
        test_batch_conversion,
        test_error_handling,
        test_edge_cases,
        test_performance,
        test_api_documentation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = test()
            if result is False:  # Some tests return False on failure
                failed += 1
            else:
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {str(e)}")
            failed += 1
    
    print("=" * 50)
    print(f"📊 Test Summary:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")

def test_specific_endpoint(endpoint, method="GET", data=None):
    """Test a specific endpoint with detailed output."""
    print(f"Testing {method} {endpoint}...")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ Endpoint working correctly")
        else:
            print("❌ Endpoint failed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("🌐 API is running and accessible!")
            run_all_tests()
        else:
            print("❌ API is not responding correctly")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on http://localhost:8000")
        print("💡 Start the API with: python -m uvicorn main:app --reload") 