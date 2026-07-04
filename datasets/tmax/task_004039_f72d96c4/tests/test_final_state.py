# test_final_state.py

import os
import json
import time
import urllib.request
import re
import pytest
import redis
from bs4 import BeautifulSoup

def test_nginx_and_processing():
    # Connect to redis
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
        r.ping()
    except redis.ConnectionError:
        pytest.fail("Redis is not running or not accessible on 127.0.0.1:6379")

    # Read corpora
    clean_path = '/workspace/data/clean.jsonl'
    evil_path = '/workspace/data/evil.jsonl'

    assert os.path.isfile(clean_path), f"Missing {clean_path}"
    assert os.path.isfile(evil_path), f"Missing {evil_path}"

    with open(clean_path, 'r') as f:
        clean_lines = f.read().splitlines()
    with open(evil_path, 'r') as f:
        evil_lines = f.read().splitlines()

    # Clear redis lists for testing
    r.delete('raw_data')
    r.delete('clean_data')

    # POST to nginx
    for line in clean_lines + evil_lines:
        req = urllib.request.Request('http://127.0.0.1:8080/ingest', data=line.encode('utf-8'), method='POST')
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status in (200, 201, 202, 204), f"Unexpected status: {response.status}"
        except Exception as e:
            pytest.fail(f"Failed to POST to Nginx at http://127.0.0.1:8080/ingest: {e}. Is Nginx and Flask configured and running?")

    # Wait for processing
    timeout = 15
    start_time = time.time()
    while time.time() - start_time < timeout:
        if r.llen('raw_data') == 0:
            break
        time.sleep(0.5)

    assert r.llen('raw_data') == 0, "Worker did not process all raw_data in time. Is worker.py running?"

    # Check clean_data
    clean_data_raw = r.lrange('clean_data', 0, -1)
    clean_data_parsed = []
    for item in clean_data_raw:
        try:
            clean_data_parsed.append(json.loads(item))
        except:
            pass

    clean_ids_expected = set()
    for line in clean_lines:
        try:
            clean_ids_expected.add(json.loads(line)['id'])
        except:
            pass

    evil_ids_expected = set()
    for line in evil_lines:
        # Evil lines might have broken unicode, so we extract id with regex
        m = re.search(r'"id"\s*:\s*(\d+)', line)
        if m:
            evil_ids_expected.add(int(m.group(1)))

    actual_ids = set([item.get('id') for item in clean_data_parsed if 'id' in item])

    missing_clean = clean_ids_expected - actual_ids
    bypassed_evil = evil_ids_expected.intersection(actual_ids)

    assert not missing_clean, f"{len(missing_clean)} of {len(clean_ids_expected)} clean modified or rejected. Missing IDs: {missing_clean}"
    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_ids_expected)} evil bypassed. Bypassed IDs: {bypassed_evil}"

def test_html_report():
    report_path = '/workspace/report.html'
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist"

    with open(report_path, 'r') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    h1 = soup.find('h1')
    assert h1 and h1.text.strip() == "Sampled IDs", "Missing or incorrect <h1> element in report.html"

    ul = soup.find('ul')
    assert ul, "Missing <ul> element in report.html"

    lis = ul.find_all('li')
    assert lis, "Missing <li> elements in report.html"

    # Extract expected groups and IDs from clean.jsonl
    with open('/workspace/data/clean.jsonl', 'r') as f:
        clean_lines = f.read().splitlines()

    groups = {}
    for line in clean_lines:
        try:
            obj = json.loads(line)
            grp = obj['group']
            if grp not in groups:
                groups[grp] = []
            if len(groups[grp]) < 2:
                groups[grp].append(obj['id'])
        except:
            pass

    expected_lis = []
    for grp in sorted(groups.keys()):
        ids_str = ", ".join(map(str, groups[grp]))
        expected_lis.append(f"Group {grp}: {ids_str}")

    actual_lis = [li.text.strip() for li in lis]

    assert actual_lis == expected_lis, f"HTML report lists do not match expected.\nExpected: {expected_lis}\nActual: {actual_lis}"