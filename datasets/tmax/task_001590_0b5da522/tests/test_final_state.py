# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_uptime_monitor_c_exists():
    assert os.path.exists('/home/user/uptime_monitor.c'), "uptime_monitor.c does not exist"

def test_setup_env_sh_exists_and_executable():
    path = '/home/user/setup_env.sh'
    assert os.path.exists(path), "setup_env.sh does not exist"
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, "setup_env.sh is not executable"

def test_vm_data_img_exists_and_ext4():
    path = '/home/user/vm_data.img'
    assert os.path.exists(path), "vm_data.img does not exist"

    # Check if it's an ext4 filesystem
    result = subprocess.run(['file', path], capture_output=True, text=True)
    assert 'ext4 filesystem data' in result.stdout, f"vm_data.img is not an ext4 filesystem: {result.stdout}"

def test_simulated_fstab():
    path = '/home/user/simulated_fstab'
    assert os.path.exists(path), "simulated_fstab does not exist"

    with open(path, 'r') as f:
        content = f.read().strip()

    # Matches: /home/user/vm_data.img /mnt/vm_data ext4 loop 0 0
    pattern = r'^\/home\/user\/vm_data\.img\s+\/mnt\/vm_data\s+ext4\s+loop\s+0\s+0$'
    assert re.search(pattern, content, re.MULTILINE), f"simulated_fstab does not contain the correct mount entry. Content: {content}"

def test_vm_logrotate_conf():
    path = '/home/user/vm_logrotate.conf'
    assert os.path.exists(path), "vm_logrotate.conf does not exist"

    with open(path, 'r') as f:
        content = f.read()

    assert '/home/user/vm_uptime.log' in content, "Logrotate config missing target log file"
    assert 'daily' in content, "Logrotate config missing 'daily'"
    assert re.search(r'rotate\s+4', content), "Logrotate config missing 'rotate 4'"
    assert 'compress' in content, "Logrotate config missing 'compress'"
    assert 'missingok' in content, "Logrotate config missing 'missingok'"

def test_vm_uptime_log_initial_execution():
    path = '/home/user/vm_uptime.log'
    assert os.path.exists(path), "vm_uptime.log does not exist"

    with open(path, 'r') as f:
        content = f.read()

    assert 'STATUS: OK' in content, "vm_uptime.log does not contain 'STATUS: OK'. Did you run ./uptime_monitor 8080?"

def test_uptime_monitor_executable_behavior():
    executable = '/home/user/uptime_monitor'
    assert os.path.exists(executable), "uptime_monitor executable does not exist"
    assert os.access(executable, os.X_OK), "uptime_monitor is not executable"

    log_path = '/home/user/vm_uptime.log'

    # Run against a closed port
    result = subprocess.run([executable, '9999'])
    assert result.returncode == 1, "uptime_monitor should exit with code 1 for a closed port"

    with open(log_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, "vm_uptime.log is empty"
    assert lines[-1].strip() == 'STATUS: FAIL', "uptime_monitor did not append 'STATUS: FAIL' to vm_uptime.log for a failed connection"