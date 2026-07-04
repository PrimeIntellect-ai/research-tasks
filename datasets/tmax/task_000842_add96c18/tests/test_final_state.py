# test_final_state.py
import os
import glob
import json
import subprocess
import urllib.request
import tempfile
import re
import uuid
from datetime import datetime
import pytest

CLEAN_CORPUS_DIR = "/app/data/corpus_clean/"
EVIL_CORPUS_DIR = "/app/data/corpus_evil/"
SANITIZER_SCRIPT = "/home/user/sanitizer.py"
READY_FLAG = "/home/user/ready.flag"

def test_ready_flag_exists():
    assert os.path.exists(READY_FLAG), f"Ready flag {READY_FLAG} not found. Did you finish the task?"

def test_sanitizer_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.jsonl"))
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []

    for fpath in clean_files:
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tmp:
            out_path = tmp.name

        try:
            subprocess.run(["python3", SANITIZER_SCRIPT, fpath, out_path], check=True, capture_output=True, timeout=10)

            with open(fpath, "r") as orig:
                orig_lines = [line.strip() for line in orig if line.strip()]
            with open(out_path, "r") as out:
                out_lines = [line.strip() for line in out if line.strip()]

            if len(orig_lines) != len(out_lines):
                failed_files.append(os.path.basename(fpath))
        except Exception:
            failed_files.append(os.path.basename(fpath))
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified/failed: {failed_files}"

def test_sanitizer_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.jsonl"))
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []

    for fpath in evil_files:
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as tmp:
            out_path = tmp.name

        try:
            subprocess.run(["python3", SANITIZER_SCRIPT, fpath, out_path], check=True, capture_output=True, timeout=10)

            with open(out_path, "r") as out:
                out_lines = [line.strip() for line in out if line.strip()]

            for line in out_lines:
                try:
                    record = json.loads(line)
                    # Check id
                    uuid.UUID(record.get("id", ""), version=4)

                    # Check timestamp
                    ts_str = record.get("timestamp", "")
                    if ts_str.endswith("Z"):
                        ts_str = ts_str[:-1] + "+00:00"
                    datetime.fromisoformat(ts_str)

                    # Check host
                    if not re.match(r"^[a-zA-Z0-9\-]+$", record.get("host", "")):
                        raise ValueError("Invalid host")

                    # Check cpu_usage
                    cpu = record.get("cpu_usage")
                    if not isinstance(cpu, (int, float)) or not (0.0 <= cpu <= 100.0):
                        raise ValueError("Invalid cpu_usage")
                except Exception:
                    failed_files.append(os.path.basename(fpath))
                    break

        except Exception:
            failed_files.append(os.path.basename(fpath))
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {failed_files}"

def test_etl_daemon_sink_verification():
    try:
        req = urllib.request.Request("http://127.0.0.1:9090/verify_state")
        with urllib.request.urlopen(req, timeout=15) as response:
            assert response.status == 200, "Sink verification failed. Status was not 200."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Sink verification endpoint returned HTTP error: {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to verify ETL daemon state with Sink: {e}")