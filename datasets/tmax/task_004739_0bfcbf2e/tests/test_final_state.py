# test_final_state.py
import os
import json
import pytest

def test_report_json_exists():
    report_path = "/home/user/profiler_output/report.json"
    assert os.path.isfile(report_path), f"The file {report_path} does not exist. The environment configuration or output path is incorrect."

def test_report_json_content():
    report_path = "/home/user/profiler_output/report.json"
    assert os.path.isfile(report_path), "report.json is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"report.json is not valid JSON: {e}")

    assert isinstance(data, list), "The root of report.json must be a JSON array."

    expected_metrics = {}
    mock_proc_dir = "/home/user/mock_proc"

    for pid in ["100", "200", "300"]:
        stat_file = os.path.join(mock_proc_dir, pid, "stat")
        diff_file = os.path.join(mock_proc_dir, pid, "diff.txt")

        if not os.path.exists(stat_file) or not os.path.exists(diff_file):
            continue

        with open(stat_file, "r") as f:
            stat_content = f.read().strip()

        # Parse utime correctly by finding the last parenthesis
        last_paren = stat_content.rfind(')')
        if last_paren != -1:
            fields = stat_content[last_paren+1:].split()
            # The 3rd field in stat is fields[0] after the last ')', so 14th field (utime) is fields[11]
            utime = int(fields[11])
        else:
            pytest.fail(f"Malformed stat file for PID {pid}")

        with open(diff_file, "r") as f:
            diff_content = f.read().strip()
            uptime_diff = int(diff_content.split('=')[1])

        if uptime_diff == 0:
            metric = 0
        else:
            metric = utime // uptime_diff

        expected_metrics[pid] = metric

    assert len(data) == len(expected_metrics), f"Expected {len(expected_metrics)} objects in JSON, found {len(data)}. Ensure directory traversal avoids symlink loops."

    actual_metrics = {str(item.get("pid")): item.get("metric") for item in data}

    for pid, expected_metric in expected_metrics.items():
        assert pid in actual_metrics, f"PID {pid} is missing from report.json. Symlink loop or parsing issue might be present."
        assert actual_metrics[pid] == expected_metric, f"PID {pid} has incorrect metric. Expected {expected_metric}, got {actual_metrics[pid]}. Check parsing logic and division by zero handling."