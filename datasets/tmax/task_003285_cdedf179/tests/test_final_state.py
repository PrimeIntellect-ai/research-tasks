# test_final_state.py

import os
import sys
import json
import urllib.request
import urllib.error
import pytest

# Add app directory to sys.path to import sanitizer
sys.path.insert(0, "/home/user/app")

try:
    from sanitizer import process_translations, write_stratified_sample
except ImportError:
    pass  # Let the tests fail if the module or functions are missing

def test_sanitizer_adversarial_corpus():
    clean_dir = "/home/user/corpus/clean/"
    evil_dir = "/home/user/corpus/evil/"
    base_csv_path = "/home/user/app/base_en.csv"

    assert os.path.exists(clean_dir), f"Clean directory missing: {clean_dir}"
    assert os.path.exists(evil_dir), f"Evil directory missing: {evil_dir}"
    assert os.path.exists(base_csv_path), f"Base CSV missing: {base_csv_path}"

    import pandas as pd

    clean_failed = []
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        try:
            df = process_translations(path, base_csv_path)
            if not isinstance(df, pd.DataFrame) or len(df) == 0:
                clean_failed.append(f)
        except Exception:
            clean_failed.append(f)

    evil_failed = []
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        try:
            df = process_translations(path, base_csv_path)
            if isinstance(df, pd.DataFrame) and len(df) > 0:
                evil_failed.append(f)
        except Exception:
            pass  # Handled validation error is acceptable

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_write_stratified_sample(tmp_path):
    import pandas as pd
    df = pd.DataFrame({
        'string_id': ['s1', 's2', 's3', 's4', 's5'],
        'context_tag': ['nav', 'nav', 'nav', 'btn', 'btn'],
        'translation': ['t1', 't2', 't3', 't4', 't5']
    })

    out_path = str(tmp_path / "sample.json")
    write_stratified_sample(df, out_path)

    assert os.path.exists(out_path), "write_stratified_sample did not create the output JSON file"

    with open(out_path, 'r') as f:
        data = json.load(f)

    # Check if data is a list of dicts or similar, and check counts
    # If saved via pandas to_json, it might be a list of records
    if isinstance(data, dict) and 'context_tag' in data:
        # Orient columns or index
        df_out = pd.read_json(out_path)
    else:
        df_out = pd.read_json(out_path, orient='records' if isinstance(data, list) else None)

    counts = df_out['context_tag'].value_counts()
    assert counts.get('nav', 0) == 2, "Expected exactly 2 samples for 'nav' context"
    assert counts.get('btn', 0) == 2, "Expected exactly 2 samples for 'btn' context"

def test_services_composition():
    # Test Nginx -> Flask -> Redis flow
    # We will just test if Nginx is listening on 8080 and routing to Flask (5000)
    url = "http://127.0.0.1:8080/api/"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            assert status in [200, 400, 404, 405], f"Unexpected status code: {status}"
    except urllib.error.HTTPError as e:
        assert e.code in [200, 400, 404, 405], f"Unexpected HTTP error code: {e.code}"
    except urllib.error.URLError:
        pytest.fail("Nginx is not proxying to Flask correctly on port 8080")