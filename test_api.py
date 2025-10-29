"""
Test script for the Music Year Prediction API
"""
import time
import json

# Wait for server to be ready
print("Waiting for server to start...")
time.sleep(3)

try:
    import requests

    BASE_URL = "http://localhost:8000"

    # Test 1: Health Check
    print("\n" + "="*60)
    print("TEST 1: Health Check (GET /health)")
    print("="*60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test 2: Prediction - 1970s Rock Song (CCR)
    print("\n" + "="*60)
    print("TEST 2: Predict 1970s Rock Song (CCR - Have You Ever Seen The Rain)")
    print("="*60)
    test_data_1970s = {
        "acousticness": 0.0936,
        "danceability": 0.743,
        "energy": 0.47,
        "instrumentalness": 0.0000315,
        "liveness": 0.186,
        "loudness": -13.154,
        "speechiness": 0.029,
        "tempo": 116.122,
        "valence": 0.89,
        "duration_ms": 160333.0,
        "key": 0.0,
        "mode": 1.0
    }
    response = requests.post(f"{BASE_URL}/predict", json=test_data_1970s)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print(f"\nActual Year: 1970")
    print(f"Predicted Year: {result['predicted_year']}")
    print(f"Error: {abs(1970 - result['predicted_year'])} years")

    # Test 3: Prediction - 1920s Classical (Rachmaninoff)
    print("\n" + "="*60)
    print("TEST 3: Predict 1920s Classical (Rachmaninoff - Piano Concerto)")
    print("="*60)
    test_data_1920s = {
        "acousticness": 0.982,
        "danceability": 0.279,
        "energy": 0.211,
        "instrumentalness": 0.878,
        "liveness": 0.665,
        "loudness": -20.096,
        "speechiness": 0.0366,
        "tempo": 80.954,
        "valence": 0.0594,
        "duration_ms": 831667.0,
        "key": 10.0,
        "mode": 1.0
    }
    response = requests.post(f"{BASE_URL}/predict", json=test_data_1920s)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print(f"\nActual Year: 1921")
    print(f"Predicted Year: {result['predicted_year']}")
    print(f"Error: {abs(1921 - result['predicted_year'])} years")

    # Test 4: Prediction - 2020 Pop (24kGoldn)
    print("\n" + "="*60)
    print("TEST 4: Predict 2020 Pop Song (24kGoldn - Mood)")
    print("="*60)
    test_data_2020 = {
        "acousticness": 0.221,
        "danceability": 0.7,
        "energy": 0.722,
        "instrumentalness": 0.0,
        "liveness": 0.272,
        "loudness": -3.558,
        "speechiness": 0.0369,
        "tempo": 90.989,
        "valence": 0.756,
        "duration_ms": 140526.0,
        "key": 7.0,
        "mode": 0.0
    }
    response = requests.post(f"{BASE_URL}/predict", json=test_data_2020)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    print(f"\nActual Year: 2020")
    print(f"Predicted Year: {result['predicted_year']}")
    print(f"Error: {abs(2020 - result['predicted_year'])} years")

    # Test 5: Invalid Input (Missing Fields)
    print("\n" + "="*60)
    print("TEST 5: Invalid Input (Missing Required Fields)")
    print("="*60)
    invalid_data = {
        "acousticness": 0.5,
        "danceability": 0.7
    }
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED!")
    print("="*60)

except ImportError:
    print("ERROR: requests module not installed")
    print("Install with: pip install requests")
except requests.exceptions.ConnectionError:
    print("ERROR: Could not connect to API")
    print("Make sure the server is running with: uvicorn app.main:app --reload --port 8000")
except Exception as e:
    print(f"ERROR: {e}")

