"""
Quick test script for Docker container
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("Testing Music Year Prediction API in Docker")
print("=" * 60)

# Test 1: Health Check
print("\n1. Health Check")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Model Loaded: {data.get('model_loaded')}")
    print(f"Status: {data.get('status')}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 2: Prediction (1970s Rock)
print("\n2. Prediction Test (1970s Rock Song)")
test_data = {
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

try:
    response = requests.post(f"{BASE_URL}/predict", json=test_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Predicted Year: {result['predicted_year']}")
    print(f"Actual Year: 1970")
    print(f"Error: {abs(1970 - result['predicted_year'])} years")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: Invalid Input
print("\n3. Invalid Input Test")
invalid_data = {"acousticness": 0.5}
try:
    response = requests.post(f"{BASE_URL}/predict", json=invalid_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 422:
        print("[PASS] Validation working correctly (422 error)")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 60)
print("Docker API tests complete!")

