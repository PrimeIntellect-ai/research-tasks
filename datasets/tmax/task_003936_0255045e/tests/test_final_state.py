# test_final_state.py

import os
import subprocess
import json
import re
import pytest

def test_makefile_fixed_and_builds():
    app_dir = "/app/net-sniff-processor-v1.2.0"
    binary_path = os.path.join(app_dir, "net-sniff")

    # Clean up any existing binary to ensure we are testing the build process
    if os.path.exists(binary_path):
        os.remove(binary_path)

    result = subprocess.run(
        ["make", "build"],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"make build failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.isfile(binary_path), f"make build succeeded but {binary_path} was not created."


def test_redactor_binary_exists():
    binary_path = "/home/user/redactor"
    assert os.path.isfile(binary_path), f"The redactor binary at {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The redactor binary at {binary_path} is not executable."


def run_redactor_on_corpus(corpus_dir):
    binary_path = "/home/user/redactor"
    results = {}

    for filename in os.listdir(corpus_dir):
        filepath = os.path.join(corpus_dir, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, 'r') as f:
            args = [line.strip() for line in f if line.strip()]

        env = os.environ.copy()
        env["TARGET_SCRIPT"] = "/bin/cat"

        cmd = [binary_path] + args
        result = subprocess.run(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        results[filename] = {
            'args': args,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip(),
            'returncode': result.returncode
        }

    return results


def test_clean_corpus():
    clean_dir = "/app/tests/corpus/clean"
    results = run_redactor_on_corpus(clean_dir)

    failed_files = []
    for filename, data in results.items():
        if data['returncode'] != 0:
            failed_files.append(f"{filename} (crashed)")
            continue

        try:
            output_json = json.loads(data['stdout'])
        except json.JSONDecodeError:
            failed_files.append(f"{filename} (invalid JSON output)")
            continue

        if output_json != data['args']:
            failed_files.append(f"{filename} (modified clean arguments)")

    assert not failed_files, f"{len(failed_files)} of {len(results)} clean files modified or failed: {', '.join(failed_files)}"


def test_evil_corpus():
    evil_dir = "/app/tests/corpus/evil"
    results = run_redactor_on_corpus(evil_dir)

    akia_pattern = re.compile(r'AKIA[A-Z0-9]{16}')
    password_pattern = re.compile(r'PASSWORD=[^ ]+')

    failed_files = []
    for filename, data in results.items():
        if data['returncode'] != 0:
            failed_files.append(f"{filename} (crashed)")
            continue

        try:
            output_json = json.loads(data['stdout'])
        except json.JSONDecodeError:
            failed_files.append(f"{filename} (invalid JSON output)")
            continue

        # Check if any secrets leaked into the output
        leaked = False
        for item in output_json:
            if akia_pattern.search(item) or password_pattern.search(item):
                leaked = True
                break

        if leaked:
            failed_files.append(f"{filename} (failed to redact secret)")

    assert not failed_files, f"{len(failed_files)} of {len(results)} evil files bypassed redaction or failed: {', '.join(failed_files)}"