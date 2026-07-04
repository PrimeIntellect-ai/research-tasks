# test_final_state.py
import os
import glob
import urllib.request
import urllib.error
import pytest
import datetime
import subprocess
import time

def test_proxy_pid_file():
    pid_file = "/home/user/proxy.pid"
    assert os.path.exists(pid_file), f"{pid_file} does not exist"
    with open(pid_file, "r") as f:
        pid = f.read().strip()
    assert pid.isdigit(), f"{pid_file} does not contain a valid PID"

def test_evil_corpus():
    evil_files = glob.glob("/home/user/corpus/evil/*.txt")
    assert len(evil_files) > 0, "No evil corpus files found in /home/user/corpus/evil"

    bypassed = []
    for f in evil_files:
        with open(f, "r") as file:
            uri = file.read().strip()
        # Encode spaces to avoid urllib errors
        uri = uri.replace(" ", "%20")
        url = f"http://127.0.0.1:8080{uri}"
        try:
            req = urllib.request.Request(url)
            urllib.request.urlopen(req, timeout=2)
            bypassed.append(os.path.basename(f))
        except urllib.error.HTTPError as e:
            if e.code != 403:
                bypassed.append(os.path.basename(f))
        except Exception:
            bypassed.append(os.path.basename(f))

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"

def test_clean_corpus_and_timezone():
    clean_files = glob.glob("/home/user/corpus/clean/*.txt")
    assert len(clean_files) > 0, "No clean corpus files found in /home/user/corpus/clean"

    modified = []
    for f in clean_files:
        with open(f, "r") as file:
            uri = file.read().strip()
        uri = uri.replace(" ", "%20")
        url = f"http://127.0.0.1:8080{uri}"
        try:
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req, timeout=2)
            if response.status != 200:
                modified.append(os.path.basename(f))
                continue
            body = response.read().decode('utf-8')
            if "Time: " not in body or "MISSING" in body:
                modified.append(os.path.basename(f))
                continue
            time_str = body.split("Time: ")[1].strip()
            # Basic validation of YYYY-MM-DD HH:MM:SS format
            try:
                datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                modified.append(os.path.basename(f))
        except Exception:
            modified.append(os.path.basename(f))

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified or failed: {', '.join(modified)}"

def test_failover():
    # Find and kill backend A (8081)
    try:
        pids = subprocess.check_output(["pgrep", "-f", "backend.py 8081"]).decode().strip().split()
        for pid in pids:
            subprocess.run(["kill", "-9", pid])
    except subprocess.CalledProcessError:
        pass # Process might not exist

    time.sleep(1)

    # Test proxy still works and routes to backend B (8082)
    url = "http://127.0.0.1:8080/api/v1/status"
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req, timeout=3)
        assert response.status == 200
        body = response.read().decode('utf-8')
        assert "Backend 8082" in body, "Failover to Backend B failed, response did not indicate Backend 8082"
    except Exception as e:
        pytest.fail(f"Failover test failed: {e}")