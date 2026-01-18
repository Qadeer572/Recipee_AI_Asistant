"""
Test script to verify the Django app is working
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_recipe_search():
    """Test searching for a recipe by name"""
    print("\n" + "="*60)
    print("Testing Recipe Search (by name)")
    print("="*60)
    
    payload = {
        "query": "Chicken Biryani",
        "type": "recipe"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/search/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print(f"✅ Success!")
            print(f"Query: {result.get('query')}")
            print(f"Result preview: {result.get('result', '')[:200]}...")
        else:
            print(f"❌ Failed!")
            print(f"Error: {result.get('error')}")
        
        return result.get('success', False)
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_ingredients_search():
    """Test searching by ingredients"""
    print("\n" + "="*60)
    print("Testing Recipe Search (by ingredients)")
    print("="*60)
    
    payload = {
        "query": "chicken, tomatoes, rice",
        "type": "ingredients"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/search/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print(f"✅ Success!")
            print(f"Query: {result.get('query')}")
            print(f"Result preview: {result.get('result', '')[:200]}...")
        else:
            print(f"❌ Failed!")
            print(f"Error: {result.get('error')}")
        
        return result.get('success', False)
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("🧪 RECIPE AI DJANGO APP - TEST SUITE")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print("="*60)
    
    # Run tests
    results = {
        "Health Check": test_health_check(),
        "Recipe Search": test_recipe_search(),
        "Ingredients Search": test_ingredients_search()
    }
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*60)


if __name__ == "__main__":
    main()
