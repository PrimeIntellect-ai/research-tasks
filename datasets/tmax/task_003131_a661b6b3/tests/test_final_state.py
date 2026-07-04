# test_final_state.py
import os
import time
import subprocess

def test_operator_sh_exists_and_executable():
    path = '/home/user/operator.sh'
    assert os.path.exists(path), f"{path} does not exist"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_operator_running():
    try:
        output = subprocess.check_output(['pgrep', '-f', 'operator.sh']).decode().strip()
        assert output, "operator.sh is not running in the background"
    except subprocess.CalledProcessError:
        assert False, "operator.sh is not running in the background"

def test_operator_behavior():
    src_dir = '/home/user/k8s/src'
    live_dir = '/home/user/k8s/live'
    archive_dir = '/home/user/k8s/archive'

    assert os.path.isdir(src_dir), f"{src_dir} does not exist. The script might not have created it."
    assert os.path.isdir(live_dir), f"{live_dir} does not exist. The script might not have created it."
    assert os.path.isdir(archive_dir), f"{archive_dir} does not exist. The script might not have created it."

    app1_src = os.path.join(src_dir, 'app1.yaml')
    app2_src = os.path.join(src_dir, 'app2.yaml')

    # Create test files
    with open(app1_src, 'w') as f:
        f.write("# DEPLOY_STATE: active\nkind: Deployment\n")

    with open(app2_src, 'w') as f:
        f.write("# DEPLOY_STATE: pending\nkind: Service\n")

    # Wait for the operator to process
    time.sleep(3)

    app1_live = os.path.join(live_dir, 'app1.yaml')
    app2_live = os.path.join(live_dir, 'app2.yaml')

    assert os.path.islink(app1_live), f"{app1_live} should be a symlink for active state"

    # Check symlink target
    target = os.readlink(app1_live)
    abs_target = target if os.path.isabs(target) else os.path.abspath(os.path.join(live_dir, target))
    assert abs_target == app1_src, f"{app1_live} should point to {app1_src}"

    assert not os.path.exists(app2_live), f"{app2_live} should not exist for pending state"

    status_file = '/home/user/operator.status'
    assert os.path.exists(status_file), f"{status_file} does not exist"

    with open(status_file, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) == 2, f"{status_file} should have exactly two lines"
    assert lines[0].isdigit(), f"First line of {status_file} is not a valid PID"
    assert lines[1].isdigit(), f"Second line of {status_file} is not a valid Unix timestamp"

    initial_timestamp = int(lines[1])

    # Modify app1 to archived
    with open(app1_src, 'w') as f:
        f.write("# DEPLOY_STATE: archived\nkind: Deployment\n")

    # Wait for the operator to process the change
    time.sleep(3)

    assert not os.path.exists(app1_live), f"{app1_live} symlink should have been removed after state changed to archived"

    app1_archive = os.path.join(archive_dir, 'app1.yaml')
    assert os.path.exists(app1_archive), f"{app1_archive} should exist after archiving"
    assert os.path.isfile(app1_archive) and not os.path.islink(app1_archive), f"{app1_archive} should be a regular file, not a symlink"

    assert not os.path.exists(app1_src), f"{app1_src} should have been moved from src directory"

    with open(status_file, 'r') as f:
        lines2 = f.read().splitlines()

    assert len(lines2) == 2, f"{status_file} should have exactly two lines"
    new_timestamp = int(lines2[1])
    assert new_timestamp > initial_timestamp, f"Timestamp in {status_file} did not increase, the loop might not be running"