# test_final_state.py

import os
import json
import subprocess
import pytest

def test_test_pipeline_script_exists_and_executable():
    script_path = "/home/user/test_pipeline.sh"
    assert os.path.isfile(script_path), f"Test script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Test script {script_path} is not executable."

def test_test_pipeline_execution():
    script_path = "/home/user/test_pipeline.sh"
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_pipeline.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_report_json_valid_and_complete():
    report_path = "/home/user/diagnostics/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} is not valid JSON.")

    assert isinstance(data, list), "Report JSON is not a list."
    assert len(data) == 5, f"Report JSON contains {len(data)} entries, expected exactly 5."

def test_root_cause_logic():
    report_path = "/home/user/diagnostics/report.json"
    with open(report_path, 'r') as f:
        data = json.load(f)

    results = {item['file']: item['root_cause'] for item in data}

    assert 'app err 1.log' in results, "Missing entry for 'app err 1.log'"
    assert results['app err 1.log'] == 'E103', "Incorrect root cause for 'app err 1.log'"

    assert 'app err 2.log' in results, "Missing entry for 'app err 2.log'"
    assert results['app err 2.log'] in ['E201', 'E202'], "Incorrect root cause for 'app err 2.log'"

    assert 'sys log 3.log' in results, "Missing entry for 'sys log 3.log'"
    assert results['sys log 3.log'] == 'E302', "Incorrect root cause for 'sys log 3.log'"

    assert 'db err 4.log' in results, "Missing entry for 'db err 4.log'"
    assert results['db err 4.log'] in ['E401', 'E402', 'E403'], "Incorrect root cause for 'db err 4.log'"

    assert 'net log 5.log' in results, "Missing entry for 'net log 5.log'"
    assert results['net log 5.log'] == 'E501', "Incorrect root cause for 'net log 5.log'"

def test_run_pipeline_fixes():
    script_path = "/home/user/diagnostics/run_pipeline.sh"
    with open(script_path, 'r') as f:
        content = f.read()

    assert "$(ls" not in content, "run_pipeline.sh still uses $(ls ...) which breaks on spaces."
    assert ' "$' in content or '"${' in content, "run_pipeline.sh does not appear to quote the filename variable properly."

def test_parse_trace_locking():
    script_path = "/home/user/diagnostics/parse_trace.py"
    with open(script_path, 'r') as f:
        content = f.read()

    assert "fcntl" in content and ("flock" in content or "lockf" in content), "parse_trace.py does not appear to use fcntl file locking."