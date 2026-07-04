# test_final_state.py
import os
import math
import pytest
import requests

def test_admin_token_recovered():
    """
    Validates that the admin token was successfully recovered from the Git history
    and written to the correct file.
    """
    token_file = "/home/user/admin_token.txt"
    assert os.path.exists(token_file), f"Token file {token_file} was not created."

    with open(token_file, "r") as f:
        token = f.read().strip()

    expected_token = "8f92a-super-secret-admin-key"
    assert token == expected_token, f"Incorrect token found in {token_file}. Expected '{expected_token}', got '{token}'."

def test_server_running_and_correct():
    """
    Validates that the server is running on port 9090, accepts the recovered token,
    and returns the uncorrupted ticket data (confirming the C memory bug is fixed).
    """
    url = "http://127.0.0.1:9090/api/tickets"
    headers = {"Auth-Token": "8f92a-super-secret-admin-key"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server on 127.0.0.1:9090. Ensure the daemon is running in the background.")
    except requests.exceptions.Timeout:
        pytest.fail("Request to the server timed out. The server might be hung or deadlocked.")
    except Exception as e:
        pytest.fail(f"Unexpected error when connecting to server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Server did not return valid JSON. Response body: {response.text}")

    assert "status" in data, "JSON response missing 'status' field."
    assert data["status"] == "ok", f"Expected status 'ok', got '{data['status']}'"

    assert "tickets" in data, "JSON response missing 'tickets' field."
    tickets = data["tickets"]
    assert isinstance(tickets, list), "'tickets' field should be a list."
    assert len(tickets) >= 1, "'tickets' list is empty."

    ticket = tickets[0]
    assert "id" in ticket, "Ticket missing 'id' field."
    assert ticket["id"] == 1, f"Expected ticket id 1, got {ticket['id']}"

    assert "priority" in ticket, "Ticket missing 'priority' field."

    # Check if the precision loss / memory corruption bug was fixed
    priority = ticket["priority"]
    assert isinstance(priority, (int, float)), "Ticket priority should be a number."

    expected_priority = 4.50291
    # We use math.isclose to account for minor floating point differences, 
    # but it must be very close to the expected value to prove the stack corruption/truncation is fixed.
    assert math.isclose(priority, expected_priority, rel_tol=1e-5), \
        f"Ticket priority is corrupted or truncated. Expected {expected_priority}, got {priority}. The C struct/scanf bug might not be fully fixed."