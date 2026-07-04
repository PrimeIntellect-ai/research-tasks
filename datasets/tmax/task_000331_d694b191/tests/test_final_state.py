# test_final_state.py
import urllib.request
import json
import os
import pytest

def test_proxy_and_bundle_constraints():
    # 1. Fetch from reverse proxy
    url = "http://127.0.0.1:8080/latest_build"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        pytest.fail(f"Failed to fetch from proxy at {url}: {e}")

    # 2. Load original assets
    assets_path = "/home/user/assets.json"
    assert os.path.exists(assets_path), f"Original assets file missing: {assets_path}"
    with open(assets_path, "r") as f:
        assets_list = json.load(f)
        assets = {a["id"]: a for a in assets_list}

    # 3. Validate constraints
    assert isinstance(data, list), "Expected proxy response to be a JSON array of bundles"

    seen = set()
    for i, bundle in enumerate(data):
        assert isinstance(bundle, list), f"Bundle at index {i} is not a list"
        b_size = 0
        b_cats = set()
        for item_id in bundle:
            assert item_id not in seen, f"Duplicate asset found in bundles: {item_id}"
            seen.add(item_id)

            assert item_id in assets, f"Unknown asset ID found in bundle: {item_id}"
            asset = assets[item_id]
            b_size += asset["size"]

            assert asset["category"] not in b_cats, f"Category conflict in bundle {i}: category {asset['category']} appears multiple times"
            b_cats.add(asset["category"])

        assert b_size <= 10000, f"Bundle {i} exceeds capacity limit (10000): size is {b_size}"

    assert len(seen) == len(assets), f"Missing assets in bundles. Found {len(seen)} out of {len(assets)} total assets."

    # 4. Check metric threshold
    num_bundles = len(data)
    threshold = 170
    assert num_bundles <= threshold, f"Too many bundles used. Metric: {num_bundles}. Threshold: <= {threshold}."