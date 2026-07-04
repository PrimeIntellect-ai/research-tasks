# test_final_state.py
import pytest
import requests

def test_service_processing():
    url = "http://127.0.0.1:8000/process"

    test_cases = [
        {
            "payload": {
                "timestamp": "2023-10-25 08:30:00 EST",
                "message": "User admin failed to LOGIN. Code: 401!"
            },
            "expected": {
                "utc_time": "2023-10-25T13:30:00Z",
                "normalized_message": "user admin failed to login code 401",
                "is_valid": False
            }
        },
        {
            "payload": {
                "timestamp": "2024-01-01T12:00:00Z",
                "message": "Disk ERR on volume 3"
            },
            "expected": {
                "utc_time": "2024-01-01T12:00:00Z",
                "normalized_message": "disk err on volume 3",
                "is_valid": True
            }
        },
        {
            "payload": {
                "timestamp": "2023-05-15 14:00:00 PST",
                "message": "err system"
            },
            "expected": {
                "utc_time": "2023-05-15T22:00:00Z",
                "normalized_message": "err system",
                "is_valid": False
            }
        },
        {
            "payload": {
                "timestamp": "2022-12-31 23:59:59 UTC",
                "message": "Critical fail during reboot sequence 99"
            },
            "expected": {
                "utc_time": "2022-12-31T23:59:59Z",
                "normalized_message": "critical fail during reboot sequence 99",
                "is_valid": True
            }
        }
    ]

    for i, tc in enumerate(test_cases):
        try:
            response = requests.post(url, json=tc["payload"], timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to or get response from {url}: {e}")

        assert response.status_code == 200, f"Expected status code 200 for test case {i+1}, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response for test case {i+1} is not valid JSON. Response text: {response.text}")

        assert "utc_time" in data, f"Missing 'utc_time' in response for test case {i+1}"
        assert "normalized_message" in data, f"Missing 'normalized_message' in response for test case {i+1}"
        assert "is_valid" in data, f"Missing 'is_valid' in response for test case {i+1}"

        assert data["utc_time"] == tc["expected"]["utc_time"], f"Incorrect 'utc_time' for test case {i+1}. Expected {tc['expected']['utc_time']}, got {data['utc_time']}"
        assert data["normalized_message"] == tc["expected"]["normalized_message"], f"Incorrect 'normalized_message' for test case {i+1}. Expected '{tc['expected']['normalized_message']}', got '{data['normalized_message']}'"
        assert data["is_valid"] == tc["expected"]["is_valid"], f"Incorrect 'is_valid' for test case {i+1}. Expected {tc['expected']['is_valid']}, got {data['is_valid']}"