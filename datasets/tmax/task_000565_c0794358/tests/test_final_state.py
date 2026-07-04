# test_final_state.py

import os
import json
import subprocess
import unicodedata
import tempfile
import pytest

def is_safe(text):
    try:
        text.encode('utf-8')
    except UnicodeEncodeError:
        return False

    for char in text:
        if unicodedata.category(char) == 'Cn':
            return False

    try:
        result = subprocess.run(['/app/legacy_validator', text], capture_output=True, timeout=5)
        if result.returncode != 0:
            return False
    except Exception:
        return False

    return True

def run_student_script(input_path, output_path):
    script_path = "/home/user/filter_translations.py"
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    result = subprocess.run(
        ['python3', script_path, input_path, output_path],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_clean_corpus():
    clean_dir = "/truth/clean_corpus"
    assert os.path.exists(clean_dir), f"Clean corpus dir missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    assert clean_files, "No JSON files found in clean corpus"

    failed_files = []

    for filename in clean_files:
        input_path = os.path.join(clean_dir, filename)
        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            output_path = tmp.name

        try:
            run_student_script(input_path, output_path)

            with open(output_path, 'r', encoding='utf-8') as f:
                output_data = json.load(f)

            expected_data = [entry for entry in input_data if is_safe(entry.get('text', ''))]

            if len(output_data) != len(expected_data):
                failed_files.append(filename)
                continue

            expected_ids = {entry['id'] for entry in expected_data}
            output_ids = {entry['id'] for entry in output_data}

            if expected_ids != output_ids:
                failed_files.append(filename)

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified incorrectly: {', '.join(failed_files)}"

def test_evil_corpus():
    evil_dir = "/truth/evil_corpus"
    assert os.path.exists(evil_dir), f"Evil corpus dir missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert evil_files, "No JSON files found in evil corpus"

    failed_files = []

    for filename in evil_files:
        input_path = os.path.join(evil_dir, filename)
        with open(input_path, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            output_path = tmp.name

        try:
            run_student_script(input_path, output_path)

            with open(output_path, 'r', encoding='utf-8') as f:
                output_data = json.load(f)

            expected_data = [entry for entry in input_data if is_safe(entry.get('text', ''))]

            expected_ids = {entry['id'] for entry in expected_data}
            output_ids = {entry['id'] for entry in output_data}

            if expected_ids != output_ids:
                failed_files.append(filename)

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed filtering: {', '.join(failed_files)}"