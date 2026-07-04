# test_final_state.py
import os
import stat
import subprocess
import gzip

def test_capacity_planner_script():
    script_path = '/home/user/capacity_planner.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Script {script_path} is not executable."

def test_qemu_mock_running():
    try:
        output = subprocess.check_output(['pgrep', '-f', 'qemu_mock.py -vnc :2']).decode('utf-8')
        assert output.strip(), "qemu_mock.py is not running with '-vnc :2'."
    except subprocess.CalledProcessError:
        assert False, "qemu_mock.py is not running with '-vnc :2'."

def test_logrotate_conf():
    conf_path = '/home/user/rotate.conf'
    assert os.path.isfile(conf_path), f"Logrotate config {conf_path} does not exist."
    with open(conf_path, 'r') as f:
        content = f.read()

    assert '/home/user/vm_capacity.log' in content, "Log file path missing in rotate.conf."
    assert 'rotate 2' in content, "'rotate 2' missing in rotate.conf."
    assert 'compress' in content, "'compress' missing in rotate.conf."
    assert 'missingok' in content, "'missingok' missing in rotate.conf."
    assert 'size 10' in content.replace('bytes', '').replace('b', '').replace('c', ''), "Size directive for 10 bytes missing in rotate.conf."

def test_rotated_log_contents():
    rotated_log_path = '/home/user/vm_capacity.log.1.gz'
    assert os.path.isfile(rotated_log_path), f"Rotated log {rotated_log_path} does not exist. Did logrotate run properly?"

    with gzip.open(rotated_log_path, 'rt') as f:
        content = f.read()

    assert "STATUS: DOWN - ACTION: STARTING VM" in content, "First log entry missing in rotated log."
    assert "STATUS: UP - ACTION: NONE" in content, "Second log entry missing in rotated log."