# test_final_state.py
import os
import pytest

def test_summary_md_exists_and_content():
    summary_path = "/home/user/summary.md"
    assert os.path.isfile(summary_path), f"{summary_path} is missing. Did the script run successfully?"

    with open(summary_path, 'r') as f:
        content = f.read()

    expected_content = """# Configuration Divergence Report
Total Keys: 5
Divergent Keys: 4

## Divergent Details
- Key: api_url | Values: dev: http://dev.api, prod: https://api.domain.com, staging: http://staging.api
- Key: db_host | Values: dev: localhost, prod: prod-db, staging: staging-db
- Key: debug | Values: dev: true, prod: false, staging: true
- Key: retry_count | Values: dev: 3, prod: 5, staging: 3"""

    # We check if the expected lines are present to allow minor trailing whitespace differences
    for expected_line in expected_content.strip().split("\n"):
        assert expected_line in content, f"Expected line not found in {summary_path}:\n{expected_line}"

def test_pipeline_log_exists_and_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. Did the script log its progress?"

    with open(log_path, 'r') as f:
        log_content = f.read()

    expected_lines = [
        "INFO: Loaded environment: dev",
        "INFO: Loaded environment: staging",
        "INFO: Loaded environment: prod",
        "INFO: Analyzed 5 total keys. Found 4 divergent keys.",
        "INFO: Report generated at /home/user/summary.md"
    ]

    for line in expected_lines:
        assert line in log_content, f"Expected log line not found in {log_path}:\n{line}"