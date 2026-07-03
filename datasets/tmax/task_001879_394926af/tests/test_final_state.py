# test_final_state.py
import os
import subprocess
import time
import urllib.request
import hashlib
import pytest

def test_patched_server_exists_and_executable():
    patched_bin = '/home/user/patched_server'
    assert os.path.isfile(patched_bin), f"Patched binary {patched_bin} is missing."
    assert os.access(patched_bin, os.X_OK), f"Patched binary {patched_bin} is not executable."

def test_patcher_go_exists():
    patcher_go = '/home/user/patcher.go'
    assert os.path.isfile(patcher_go), f"Go source file {patcher_go} is missing."

def test_checksum_txt():
    patched_bin = '/home/user/patched_server'
    checksum_file = '/home/user/checksum.txt'

    assert os.path.isfile(checksum_file), f"Checksum file {checksum_file} is missing."

    with open(patched_bin, 'rb') as f:
        actual_checksum = hashlib.sha256(f.read()).hexdigest()

    with open(checksum_file, 'r') as f:
        written_checksum = f.read().strip()

    assert actual_checksum == written_checksum, f"Checksum in {checksum_file} does not match the actual SHA256 of {patched_bin}."

def test_patched_server_functionality():
    patched_bin = '/home/user/patched_server'

    # Start the patched server
    process = subprocess.Popen([patched_bin])

    try:
        # Wait for the server to start
        time.sleep(1.5)

        success_count = 0
        total_requests = 10

        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

        opener = urllib.request.build_opener(NoRedirectHandler)

        for i in range(total_requests):
            try:
                url = f"http://127.0.0.1:8080/redirect?path=test{i}"
                req = urllib.request.Request(url)
                response = opener.open(req, timeout=2)

                # If it didn't redirect automatically, the status code should be 302
                if response.status == 302:
                    location = response.getheader('Location')
                    expected_location = f"http://redacted-secure-domain.com/test{i}"
                    if location == expected_location:
                        success_count += 1
            except urllib.error.HTTPError as e:
                if e.code == 302:
                    location = e.headers.get('Location')
                    expected_location = f"http://redacted-secure-domain.com/test{i}"
                    if location == expected_location:
                        success_count += 1
            except Exception as e:
                pass

        accuracy = success_count / float(total_requests)
        assert accuracy >= 1.0, f"Accuracy = {accuracy}. Expected >= 1.0. Server did not redirect correctly for all payloads."

    finally:
        process.terminate()
        process.wait(timeout=2)