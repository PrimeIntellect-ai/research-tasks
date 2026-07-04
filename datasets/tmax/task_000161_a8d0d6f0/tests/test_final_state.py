# test_final_state.py
import os
import socket
import subprocess
import requests
import pytest

def test_organized_docs_directory():
    org_dir = '/home/user/organized_docs'
    assert os.path.isdir(org_dir), f"Directory {org_dir} does not exist."
    files = [f for f in os.listdir(org_dir) if f.endswith('.txt')]
    assert len(files) == 3, f"Expected exactly 3 .txt files in {org_dir}, found {len(files)}."

    expected_titles = {"Architecture_Plan", "API_Reference_V2", "Database_Schema"}

    for f in files:
        filepath = os.path.join(org_dir, f)

        # Get hash using the binary
        result = subprocess.run(['/app/doc_hasher', filepath], capture_output=True, text=True)
        assert result.returncode == 0, f"doc_hasher failed on {filepath}"
        file_hash = result.stdout.strip()

        # Check filename format
        assert f.startswith(file_hash + "_"), f"Filename {f} does not start with its hash {file_hash}_"

        title_part = f[len(file_hash)+1:-4]
        assert title_part in expected_titles, f"Unexpected title part in filename: {title_part}"
        expected_titles.remove(title_part)

    assert len(expected_titles) == 0, f"Missing files for titles: {expected_titles}"

def test_http_service():
    org_dir = '/home/user/organized_docs'
    if not os.path.isdir(org_dir):
        pytest.fail(f"Directory {org_dir} does not exist.")

    files = [f for f in os.listdir(org_dir) if f.endswith('.txt')]
    assert len(files) == 3, "Prerequisite failed: exactly 3 files not found."

    for f in files:
        url = f"http://127.0.0.1:8080/{f}"
        try:
            resp = requests.get(url, timeout=2)
            assert resp.status_code == 200, f"HTTP GET {url} returned status {resp.status_code}"

            # Verify content matches
            filepath = os.path.join(org_dir, f)
            with open(filepath, 'rb') as local_f:
                local_content = local_f.read()
            assert resp.content == local_content, f"Content mismatch for {url}"
        except requests.RequestException as e:
            pytest.fail(f"HTTP request to {url} failed: {e}")

def test_tcp_metadata_service():
    org_dir = '/home/user/organized_docs'
    if not os.path.isdir(org_dir):
        pytest.fail(f"Directory {org_dir} does not exist.")

    files = [f for f in os.listdir(org_dir) if f.endswith('.txt')]
    assert len(files) == 3, "Prerequisite failed: exactly 3 files not found."

    for f in files:
        filepath = os.path.join(org_dir, f)
        result = subprocess.run(['/app/doc_hasher', filepath], capture_output=True, text=True)
        file_hash = result.stdout.strip()

        try:
            with socket.create_connection(('127.0.0.1', 9090), timeout=2) as s:
                s.sendall(f"{file_hash}\n".encode('utf-8'))
                response = b""
                while True:
                    chunk = s.recv(1024)
                    if not chunk:
                        break
                    response += chunk
                response_str = response.decode('utf-8')
                assert response_str == f"{f}\n", f"TCP service returned {repr(response_str)} instead of {repr(f + r'\n')}"
        except Exception as e:
            pytest.fail(f"TCP connection/request failed for hash {file_hash}: {e}")