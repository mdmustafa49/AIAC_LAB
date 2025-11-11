import requests
import json

# Base URL for your APIs
BASE_URL = "http://localhost:5000"

def test_task_1_api():
    """Test API from task_1"""
    print("Testing Task 1 API...")
    try:
        response = requests.get(f"{BASE_URL}/task1")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_task_2_api():
    """Test API from task_2"""
    print("\nTesting Task 2 API...")
    try:
        payload = {"data": "test_value"}
        response = requests.post(f"{BASE_URL}/task2", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

def test_task_3_api():
    """Test API from task_3"""
    print("\nTesting Task 3 API...")
    try:
        response = requests.get(f"{BASE_URL}/task3")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_task_1_api()
    test_task_2_api()
    test_task_3_api()