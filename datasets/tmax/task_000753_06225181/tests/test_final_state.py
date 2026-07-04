# test_final_state.py

import os
import subprocess
import pytest

def test_cypher_parser_installed():
    try:
        import cypher_parser
        # verify it can parse a basic query
        ast = cypher_parser.parse("MATCH (n) RETURN n")
        assert ast is not None, "cypher_parser.parse returned None"
    except ImportError:
        pytest.fail("cypher_parser could not be imported. The vendored package was not installed correctly.")
    except Exception as e:
        pytest.fail(f"cypher_parser is installed but failed to parse a simple query: {e}")

def test_query_filter_script_exists():
    script_path = "/home/user/query_filter.py"
    assert os.path.isfile(script_path), f"Query filter script not found at {script_path}"

def run_filter(input_dir, output_log):
    script_path = "/home/user/query_filter.py"
    result = subprocess.run(
        ["python3", script_path, "--input-dir", input_dir, "--output-log", output_log],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed on {input_dir} with error:\n{result.stderr}"

def parse_log(log_path):
    results = {}
    with open(log_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ': ' in line:
                filename, status = line.split(': ', 1)
                results[filename] = status
    return results

def test_adversarial_corpus():
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_log = "/tmp/test_clean.log"
    evil_log = "/tmp/test_evil.log"

    run_filter(clean_dir, clean_log)
    run_filter(evil_dir, evil_log)

    clean_results = parse_log(clean_log)
    evil_results = parse_log(evil_log)

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.cypher')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.cypher')]

    # Check clean corpus
    clean_failures = []
    for f in clean_files:
        if f not in clean_results:
            clean_failures.append(f"{f} (missing)")
        elif clean_results[f] != "ACCEPT":
            clean_failures.append(f"{f} ({clean_results[f]})")

    # Check evil corpus
    evil_failures = []
    for f in evil_files:
        if f not in evil_results:
            evil_failures.append(f"{f} (missing)")
        elif evil_results[f] != "REJECT":
            evil_failures.append(f"{f} ({evil_results[f]})")

    errors = []
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if errors:
        pytest.fail("\n".join(errors))