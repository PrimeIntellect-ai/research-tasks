# test_final_state.py

import os
import struct
import subprocess
import tempfile
import time
import urllib.request
import pytest

SANITIZER_BIN = "/home/user/sanitizer"
CLEAN_CORPUS = "/home/user/corpus/clean"
EVIL_CORPUS = "/home/user/corpus/evil"

def compress_rle(payload: bytes) -> bytes:
    try:
        s = payload.decode('utf-8')
    except UnicodeDecodeError:
        s = payload.decode('latin-1')
    res = []
    i = 0
    n = len(s)
    while i < n:
        char = s[i]
        count = 1
        while i + count < n and s[i + count] == char:
            count += 1
        if count >= 3:
            res.append(f"~{char}{count}")
            i += count
        else:
            res.append(char)
            i += 1
    return "".join(res).encode('utf-8')

def parse_bin(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    records = []
    idx = 0
    while idx < len(data):
        magic = data[idx:idx+4]
        if magic != b'\xef\xbe\xad\xde':
            break
        size = struct.unpack('<I', data[idx+4:idx+8])[0]
        payload = data[idx+8:idx+8+size]
        records.append(payload)
        idx += 8 + size
    return records

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_BIN), f"Sanitizer binary not found at {SANITIZER_BIN}"
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary at {SANITIZER_BIN} is not executable"

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.bin')]
    assert evil_files, "No evil corpus files found."

    bypassed = []
    for fname in evil_files:
        in_path = os.path.join(EVIL_CORPUS, fname)
        with tempfile.NamedTemporaryFile(suffix='.zarc', delete=False) as out_f:
            out_path = out_f.name

        try:
            subprocess.run([SANITIZER_BIN, in_path, out_path], capture_output=True, timeout=2, check=True)
            with open(out_path, 'rb') as f:
                out_data = f.read()
            if out_data != b"ZARC001\n":
                bypassed.append(fname)
        except subprocess.CalledProcessError:
            bypassed.append(fname + " (crashed/error)")
        except subprocess.TimeoutExpired:
            bypassed.append(fname + " (timeout)")
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil files bypassed sanitization: {', '.join(bypassed[:5])}"

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.bin')]
    assert clean_files, "No clean corpus files found."

    modified_or_failed = []
    for fname in clean_files:
        in_path = os.path.join(CLEAN_CORPUS, fname)
        with tempfile.NamedTemporaryFile(suffix='.zarc', delete=False) as out_f:
            out_path = out_f.name

        try:
            subprocess.run([SANITIZER_BIN, in_path, out_path], capture_output=True, timeout=2, check=True)
            with open(out_path, 'rb') as f:
                out_data = f.read()

            if not out_data.startswith(b"ZARC001\n"):
                modified_or_failed.append(fname + " (missing global header)")
                continue

            records = parse_bin(in_path)
            expected_data = b"ZARC001\n"
            for rec in records:
                comp = compress_rle(rec)
                expected_data += struct.pack('<I', len(rec)) + struct.pack('<I', len(comp)) + comp

            if out_data != expected_data:
                modified_or_failed.append(fname + " (RLE mismatch)")
        except Exception as e:
            modified_or_failed.append(fname + f" (error: {e})")
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    assert not modified_or_failed, f"{len(modified_or_failed)} of {len(clean_files)} clean files modified/failed: {', '.join(modified_or_failed[:5])}"

def test_end_to_end_integration():
    # Send a payload to the python frontend
    test_payload = b"TESTING_INTEGRATION_XXX_YYY_ZZZ_111"
    # Format as a proper record
    magic = b'\xef\xbe\xad\xde'
    size = struct.pack('<I', len(test_payload))
    bin_data = magic + size + test_payload

    req = urllib.request.Request("http://127.0.0.1:8080/", data=bin_data, method="POST")
    try:
        urllib.request.urlopen(req, timeout=2)
    except Exception as e:
        pytest.fail(f"Failed to post to frontend: {e}")

    # Wait for archiver to process
    time.sleep(3)

    archive_dir = "/home/user/logs/archive"
    zarc_files = [f for f in os.listdir(archive_dir) if f.endswith('.zarc')]

    found_expected = False
    expected_comp = compress_rle(test_payload)
    expected_chunk = struct.pack('<I', len(test_payload)) + struct.pack('<I', len(expected_comp)) + expected_comp

    for zf in zarc_files:
        with open(os.path.join(archive_dir, zf), 'rb') as f:
            content = f.read()
            if expected_chunk in content:
                found_expected = True
                break

    assert found_expected, "End-to-End integration failed: Could not find the processed payload in /home/user/logs/archive/*.zarc"