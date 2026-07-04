# test_final_state.py
import os
import stat

def test_script_exists():
    assert os.path.exists('/home/user/deploy_vm.py'), "/home/user/deploy_vm.py script is missing."

def test_deployment_directories_and_symlinks():
    v42_dir = '/home/user/deployments/v42'
    assert os.path.isdir(v42_dir), f"Deployment directory {v42_dir} is missing."

    disk_img = os.path.join(v42_dir, 'disk.img')
    assert os.path.islink(disk_img), f"{disk_img} is not a symlink."
    assert os.readlink(disk_img) == '/home/user/images/base.img', f"{disk_img} does not point to /home/user/images/base.img."

    current_link = '/home/user/deployments/current'
    assert os.path.islink(current_link), f"{current_link} is not a symlink."
    assert os.readlink(current_link) == '/home/user/deployments/v42', f"{current_link} does not point to /home/user/deployments/v42."

def test_run_sh_script():
    run_sh = '/home/user/deployments/v42/run.sh'
    assert os.path.isfile(run_sh), f"{run_sh} is missing."

    st = os.stat(run_sh)
    assert bool(st.st_mode & stat.S_IXUSR), f"{run_sh} is not executable by the user."

    with open(run_sh, 'r') as f:
        content = f.read().strip()

    expected_content = "#!/bin/bash\nqemu-system-x86_64 -m 1024 -drive file=disk.img,format=qcow2 -vnc :5"
    assert expected_content in content, f"{run_sh} does not contain the expected QEMU command."

def test_log_rotation():
    log_file = '/home/user/deployments/deploy.log'
    log_1 = log_file + '.1'
    log_2 = log_file + '.2'

    assert os.path.isfile(log_file), f"Log file {log_file} is missing."
    assert os.path.isfile(log_1), f"Rotated log file {log_1} is missing. Log rotation may have failed."
    assert os.path.isfile(log_2), f"Rotated log file {log_2} is missing. Log rotation may have failed."