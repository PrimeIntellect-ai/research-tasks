# test_final_state.py
import os
import subprocess
import re

def test_planner_executable_exists():
    assert os.path.exists('/home/user/planner'), "The executable /home/user/planner does not exist. Did you compile it?"
    assert os.access('/home/user/planner', os.X_OK), "The file /home/user/planner is not executable."

def test_planner_output_bkp_005():
    try:
        result = subprocess.run(['/home/user/planner', 'bkp_005'], capture_output=True, text=True, timeout=5)
    except Exception as e:
        assert False, f"Failed to run /home/user/planner: {e}"

    output = result.stdout.strip()

    expected_path_pattern = r"Path:\s*bkp_001\s*->\s*bkp_002\s*->\s*bkp_003\s*->\s*bkp_004\s*->\s*bkp_005"
    expected_size_pattern = r"Total Size:\s*136314880"

    assert re.search(expected_path_pattern, output), f"Output did not contain the expected path for bkp_005. Output was:\n{output}"
    assert re.search(expected_size_pattern, output), f"Output did not contain the expected total size for bkp_005. Output was:\n{output}"

def test_planner_output_bkp_003():
    try:
        result = subprocess.run(['/home/user/planner', 'bkp_003'], capture_output=True, text=True, timeout=5)
    except Exception as e:
        assert False, f"Failed to run /home/user/planner: {e}"

    output = result.stdout.strip()

    expected_path_pattern = r"Path:\s*bkp_001\s*->\s*bkp_002\s*->\s*bkp_003"
    expected_size_pattern = r"Total Size:\s*125829120"

    assert re.search(expected_path_pattern, output), f"Output did not contain the expected path for bkp_003. Output was:\n{output}"
    assert re.search(expected_size_pattern, output), f"Output did not contain the expected total size for bkp_003. Output was:\n{output}"

def test_optimize_sql():
    sql_file = '/home/user/optimize.sql'
    assert os.path.exists(sql_file), f"The file {sql_file} does not exist."

    with open(sql_file, 'r') as f:
        content = f.read().lower()

    # Check for CREATE INDEX ... ON backup_lineage
    assert "create " in content and "index " in content, f"{sql_file} does not contain a CREATE INDEX statement."
    assert "backup_lineage" in content, f"{sql_file} does not mention the backup_lineage table."
    assert "child_id" in content, f"{sql_file} does not index the child_id column, which is necessary for fast parent lookups."