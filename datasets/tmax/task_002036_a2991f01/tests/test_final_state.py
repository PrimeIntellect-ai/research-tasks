# test_final_state.py
import os
import json
import zlib
import hashlib
import subprocess
import pytest

def test_scripts_exist_and_executable():
    """Test that the required scripts exist and have correct permissions."""
    assert os.path.isfile("/home/user/migrate.py"), "/home/user/migrate.py is missing."
    assert os.path.isfile("/home/user/ci_pipeline.sh"), "/home/user/ci_pipeline.sh is missing."
    assert os.access("/home/user/ci_pipeline.sh", os.X_OK), "/home/user/ci_pipeline.sh is not executable."

def test_pipeline_execution():
    """Test running the CI pipeline script."""
    result = subprocess.run(
        ["/home/user/ci_pipeline.sh"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"ci_pipeline.sh failed with exit code {result.returncode}.\nStderr: {result.stderr}"
    assert "CI SUCCESS" in result.stdout, "ci_pipeline.sh did not print 'CI SUCCESS' to standard output."

def test_benchmark_report_structure():
    """Test the structure and types of the benchmark report."""
    report_path = "/home/user/benchmark_report.json"
    assert os.path.isfile(report_path), f"Benchmark report {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("benchmark_report.json is not valid JSON.")

    assert "total_valid" in report, "Missing 'total_valid' in benchmark report."
    assert "total_invalid" in report, "Missing 'total_invalid' in benchmark report."
    assert "records_per_second" in report, "Missing 'records_per_second' in benchmark report."

    assert isinstance(report["total_valid"], int), "'total_valid' must be an integer."
    assert isinstance(report["total_invalid"], int), "'total_invalid' must be an integer."
    assert isinstance(report["records_per_second"], (int, float)), "'records_per_second' must be a float."
    assert report["records_per_second"] > 0, "'records_per_second' should be greater than 0."

def test_data_migration_correctness():
    """Test that the data was migrated correctly according to the rules."""
    legacy_dir = "/home/user/legacy_data"
    new_dir = "/home/user/new_data"

    expected_valid = 0
    expected_invalid = 0

    for fname in os.listdir(legacy_dir):
        if fname.endswith(".jsonl"):
            with open(os.path.join(legacy_dir, fname), "r") as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    record = json.loads(line)
                    data = record["data"]
                    expected_crc = record["crc32"]

                    computed_crc = format(zlib.crc32(data.encode('utf-8')) & 0xFFFFFFFF, '08x')

                    if computed_crc == expected_crc:
                        expected_valid += 1
                        sha256_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
                        shard_dir = sha256_hash[:2]
                        expected_file = os.path.join(new_dir, shard_dir, f"{sha256_hash}.json")

                        assert os.path.isfile(expected_file), f"Missing migrated file for valid record: {expected_file}"

                        with open(expected_file, "r") as new_f:
                            new_record = json.load(new_f)
                            assert new_record.get("record_id") == sha256_hash, f"Incorrect record_id in {expected_file}"
                            assert new_record.get("content") == data, f"Incorrect content in {expected_file}"
                    else:
                        expected_invalid += 1

    # Verify benchmark report counts match the derived truth
    report_path = "/home/user/benchmark_report.json"
    with open(report_path, "r") as f:
        report = json.load(f)

    assert report["total_valid"] == expected_valid, f"Expected {expected_valid} total_valid, got {report['total_valid']}"
    assert report["total_invalid"] == expected_invalid, f"Expected {expected_invalid} total_invalid, got {report['total_invalid']}"