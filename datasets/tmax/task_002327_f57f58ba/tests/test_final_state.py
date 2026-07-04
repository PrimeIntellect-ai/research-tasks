# test_final_state.py

import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:8080"

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="module", autouse=True)
def ensure_server_running():
    # Attempt to reach the health or base endpoint, or just wait a bit
    url = f"{BASE_URL}/api/top_centrality?limit=1&offset=0"
    assert wait_for_server(url), "Server is not reachable at 127.0.0.1:8080. Did you start it?"

def test_pagination_offset_and_limit():
    # Request the first 10 items to establish ground truth
    resp_all = requests.get(f"{BASE_URL}/api/top_centrality?limit=10&offset=0")
    assert resp_all.status_code == 200, f"Expected 200 OK, got {resp_all.status_code}"

    data_all = resp_all.json()
    assert isinstance(data_all, list), "Response should be a JSON array"
    assert len(data_all) == 10, "Expected 10 items in the response for limit=10"

    # Request items 6-10
    resp_paginated = requests.get(f"{BASE_URL}/api/top_centrality?limit=5&offset=5")
    assert resp_paginated.status_code == 200, f"Expected 200 OK, got {resp_paginated.status_code}"

    data_paginated = resp_paginated.json()
    assert isinstance(data_paginated, list), "Response should be a JSON array"
    assert len(data_paginated) == 5, f"Expected 5 items, got {len(data_paginated)}"

    # The paginated items should exactly match the second half of the first 10 items
    assert data_paginated == data_all[5:10], "Pagination offset logic is incorrect. Items do not match the expected slice."

def test_pagination_out_of_bounds():
    # Request with a very high offset
    resp = requests.get(f"{BASE_URL}/api/top_centrality?limit=100&offset=99999")
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code} (server might have crashed or returned error)"

    data = resp.json()
    assert isinstance(data, list), "Response should be a JSON array"
    assert len(data) == 0, f"Expected empty array for out of bounds offset, got {len(data)} items"