# test_final_state.py
import os
import urllib.request
import urllib.error
import uuid
import pytest

def post_csv(url: str, file_path: str) -> int:
    boundary = uuid.uuid4().hex
    headers = {'Content-type': f'multipart/form-data; boundary={boundary}'}

    with open(file_path, 'rb') as f:
        file_content = f.read()

    filename = os.path.basename(file_path)

    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f'Content-Type: text/csv\r\n\r\n'
    ).encode('utf-8') + file_content + f'\r\n--{boundary}--\r\n'.encode('utf-8')

    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 500

def test_ready_file_exists():
    assert os.path.exists("/home/user/ready.txt"), "The /home/user/ready.txt file was not created by the agent."

def test_adversarial_corpus():
    clean_dir = "/app/eval/corpus/clean"
    evil_dir = "/app/eval/corpus/evil"
    url = "http://127.0.0.1:8080/upload"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    clean_failures = []
    evil_failures = []

    for fpath in clean_files:
        status = post_csv(url, fpath)
        if status != 200:
            clean_failures.append(f"{os.path.basename(fpath)} (status {status})")

    for fpath in evil_files:
        status = post_csv(url, fpath)
        if status != 406:
            evil_failures.append(f"{os.path.basename(fpath)} (status {status})")

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(clean_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))