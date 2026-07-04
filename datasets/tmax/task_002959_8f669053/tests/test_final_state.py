# test_final_state.py
import os
import re

def test_anomalies_log_content():
    log_path = '/home/user/finops_output/anomalies.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[2023-10-01] WARNING: High cost anomaly - Service: RDS, Resource: db-87654321, Cost: $550.00",
        "[2023-10-02] WARNING: High cost anomaly - Service: EC2, Resource: i-12345678, Cost: $600.00",
        "[2023-10-02] WARNING: High cost anomaly - Service: RDS, Resource: db-87654321, Cost: $550.00"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected log entry not found: '{expected}'"

    assert len(lines) == 3, f"Expected exactly 3 log entries, found {len(lines)}"

def test_symlinks_created():
    expected_symlinks = {
        '/home/user/finops_output/high_cost/db-87654321/2023-10-01.csv': '/home/user/billing_logs/2023-10-01.csv',
        '/home/user/finops_output/high_cost/db-87654321/2023-10-02.csv': '/home/user/billing_logs/2023-10-02.csv',
        '/home/user/finops_output/high_cost/i-12345678/2023-10-02.csv': '/home/user/billing_logs/2023-10-02.csv'
    }

    for link_path, target_path in expected_symlinks.items():
        assert os.path.islink(link_path), f"Symlink {link_path} does not exist or is not a symlink."
        actual_target = os.readlink(link_path)
        assert actual_target == target_path, f"Symlink {link_path} points to {actual_target}, expected {target_path}."

def test_logrotate_conf():
    conf_path = '/home/user/logrotate.conf'
    assert os.path.isfile(conf_path), f"Logrotate config {conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read()

    # Check if the block for the anomalies log exists
    assert '/home/user/finops_output/anomalies.log' in content, f"Logrotate config does not specify the correct log file."

    # Check for required directives
    assert re.search(r'\bsize\s+1k\b', content), "Logrotate config missing 'size 1k' directive."
    assert re.search(r'\brotate\s+3\b', content), "Logrotate config missing 'rotate 3' directive."
    assert re.search(r'\bcompress\b', content), "Logrotate config missing 'compress' directive."
    assert re.search(r'\bmissingok\b', content), "Logrotate config missing 'missingok' directive."