# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import json
import pytest

def test_venv_dependencies():
    pip_path = "/home/user/project/venv/bin/pip"
    assert os.path.isfile(pip_path), "Virtual environment pip not found at /home/user/project/venv/bin/pip. Did you create the venv correctly?"

    res = subprocess.run([pip_path, "freeze"], capture_output=True, text=True)
    assert res.returncode == 0, f"pip freeze failed with error: {res.stderr}"

    # Parse installed packages
    installed_packages = {}
    for line in res.stdout.splitlines():
        if "==" in line:
            pkg, ver = line.split("==", 1)
            installed_packages[pkg.lower()] = ver
        elif "@" in line:
            pkg = line.split("@")[0].strip()
            installed_packages[pkg.lower()] = "unknown"

    assert "fastapi" in installed_packages, "FastAPI is not installed in the virtual environment."
    assert "pydantic" in installed_packages, "Pydantic is not installed in the virtual environment."

def test_transcript():
    transcript_path = "/home/user/project/transcript.txt"
    assert os.path.isfile(transcript_path), f"Transcript file missing at {transcript_path}"

    with open(transcript_path, "r") as f:
        content = f.read().lower()

    keywords = ["fork", "sys", "socket", "nested"]
    missing = [kw for kw in keywords if kw not in content]
    assert not missing, f"Transcript is missing critical keywords extracted from audio: {', '.join(missing)}"

def test_api_execute():
    url = "http://localhost:8000/execute"
    script = "CHAN results\nSPAWN func1\nSEND results 42\nRECV results"
    req = urllib.request.Request(
        url, 
        data=script.encode('utf-8'), 
        headers={'Content-Type': 'text/plain'}, 
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert isinstance(data, list), "API response should be a JSON array of received values"
    except urllib.error.HTTPError as e:
        pytest.fail(f"API returned HTTP error {e.code} for a valid script.")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API on localhost:8000. Is the server running? Error: {e.reason}")
    except Exception as e:
        pytest.fail(f"Unexpected error when communicating with the API: {e}")

def test_adversarial_corpus():
    sanitizer_path = "/home/user/project/sanitizer.py"
    assert os.path.isfile(sanitizer_path), f"Sanitizer script not found at {sanitizer_path}"

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(evil_dir), "Evil corpus directory is missing"
    assert os.path.isdir(clean_dir), "Clean corpus directory is missing"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run(["python3", sanitizer_path, f], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run(["python3", sanitizer_path, f], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus verification failed:\n" + "\n".join(errors)