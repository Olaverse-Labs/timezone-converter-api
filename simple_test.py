import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test a specific endpoint and show detailed results."""
    print(f"\n🔍 Testing {method} {endpoint}")
    print("-" * 50)
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                print(f"Response: {json.dumps(json_data, indent=2)[:500]}...")
                print("✅ SUCCESS")
            except:
                print(f"Response: {response.text[:200]}...")
                print("✅ SUCCESS (non-JSON response)")
        else:
            print(f"Response: {response.text}")
            print("❌ FAILED")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def main():
    print("🧪 Simple API Test Script")
    print("=" * 60)
    
    # Test basic endpoints
    test_endpoint("/")
    test_endpoint("/timezones")
    test_endpoint("/timezones/search?q=America")
    
    # Test current time endpoints
    test_endpoint("/current/UTC")
    test_endpoint("/current/America%2FNew_York")  # URL encoded
    test_endpoint("/current?timezones=UTC,America/New_York")
    
    # Test info endpoint
    test_endpoint("/info/UTC")
    test_endpoint("/info/America%2FNew_York")  # URL encoded
    
    # Test conversion endpoints
    conversion_data = {
        "datetime": "2023-12-25 12:00:00",
        "source_timezone": "UTC",
        "target_timezone": "America/New_York"
    }
    test_endpoint("/convert", "POST", conversion_data)
    
    batch_data = {
        "conversions": [
            {
                "datetime": "2023-12-25 12:00:00",
                "source_timezone": "UTC",
                "target_timezone": "America/New_York"
            }
        ]
    }
    test_endpoint("/convert/batch", "POST", batch_data)
    
    # Test documentation
    test_endpoint("/docs")
    test_endpoint("/openapi.json")

if __name__ == "__main__":
    main() 