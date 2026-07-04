# test_final_state.py

import os
import stat

def test_auto_mount_exp_exists_and_executable():
    """Test that the expect script exists and is executable."""
    exp_path = "/home/user/auto_mount.exp"
    assert os.path.isfile(exp_path), f"The expect script {exp_path} does not exist."

    st = os.stat(exp_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The expect script {exp_path} is not executable."

def test_my_fstab_conf_exists_and_content():
    """Test that the generated configuration file exists and has the correct content."""
    conf_path = "/home/user/my_fstab.conf"
    assert os.path.isfile(conf_path), f"The configuration file {conf_path} does not exist. Did you run the expect script?"

    with open(conf_path, "r") as f:
        content = f.read().strip()

    expected_content = "/dev/vdc1 /home/user/data_backup xfs rw,noexec,nodev 0 0"
    assert content == expected_content, f"The contents of {conf_path} are incorrect.\nExpected: '{expected_content}'\nGot: '{content}'"

def test_setup_mounts_script_unmodified():
    """Test that the original setup script was not modified."""
    script_path = "/home/user/setup_mounts.sh"
    assert os.path.isfile(script_path), f"Expected script {script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()

    assert "read -p \"Enter device path: \" dev_path" in content, f"{script_path} was modified and is missing the device path prompt."
    assert "read -p \"Enter mount point: \" mount_point" in content, f"{script_path} was modified and is missing the mount point prompt."
    assert 'echo "$dev_path $mount_point $fs_type $mount_opts 0 0" > /home/user/my_fstab.conf' in content, f"{script_path} was modified and is missing the output logic."