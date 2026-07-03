# test_final_state.py
import os
import stat
import subprocess
import json
import pytest

SCRIPT_PATH = "/home/user/validate_backup.sh"
PATHS_LOG = "/home/user/paths.log"
PLAN_LOG = "/home/user/plan.log"
MONGO_PIPELINE = "/home/user/mongo_pipeline.json"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_outputs():
    # Clean up previous outputs if any
    for f in [PATHS_LOG, PLAN_LOG, MONGO_PIPELINE]:
        if os.path.exists(f):
            os.remove(f)

    # Run the script
    result = subprocess.run(
        [SCRIPT_PATH, "455", "2023-11-20"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    # Verify paths.log
    assert os.path.isfile(PATHS_LOG), f"{PATHS_LOG} was not created."
    with open(PATHS_LOG, "r") as f:
        paths = [line.strip() for line in f if line.strip()]

    expected_paths = [
        "backup_root",
        "backup_root/etc",
        "backup_root/etc/passwd",
        "backup_root/var",
        "backup_root/var/log",
        "backup_root/var/log/syslog"
    ]
    assert paths == sorted(expected_paths), f"Contents of {PATHS_LOG} do not match expected output or are not sorted."

    # Verify plan.log
    assert os.path.isfile(PLAN_LOG), f"{PLAN_LOG} was not created."
    with open(PLAN_LOG, "r") as f:
        plan_content = f.read().strip()
    assert plan_content, f"{PLAN_LOG} is empty."
    # Basic check to ensure it looks like an EXPLAIN QUERY PLAN output
    assert "SCAN" in plan_content.upper() or "SEARCH" in plan_content.upper(), f"{PLAN_LOG} does not appear to contain a valid query plan."

    # Verify mongo_pipeline.json
    assert os.path.isfile(MONGO_PIPELINE), f"{MONGO_PIPELINE} was not created."
    with open(MONGO_PIPELINE, "r") as f:
        try:
            pipeline = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{MONGO_PIPELINE} does not contain valid JSON.")

    assert isinstance(pipeline, list), "MongoDB pipeline must be a JSON array."
    assert len(pipeline) == 2, "MongoDB pipeline must have exactly 2 stages."

    stage1, stage2 = pipeline

    assert "$match" in stage1, "First stage must be a $match stage."
    assert stage1["$match"].get("tenant_id") == 455, "tenant_id in $match stage must be integer 455."
    assert stage1["$match"].get("backup_date") == "2023-11-20", "backup_date in $match stage must be '2023-11-20'."

    assert "$group" in stage2, "Second stage must be a $group stage."
    assert stage2["$group"].get("_id") == "$region", "_id in $group stage must be '$region'."

    total_bytes = stage2["$group"].get("total_bytes")
    assert total_bytes is not None, "Missing 'total_bytes' field in $group stage."
    assert total_bytes.get("$sum") == "$file_size_bytes", "'total_bytes' must be the sum of '$file_size_bytes'."