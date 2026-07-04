# test_final_state.py

import os
import subprocess
import hashlib
import stat

def test_directories_exist():
    dirs = [
        "/home/user/manifests/raw",
        "/home/user/manifests/active",
        "/home/user/manifests/versions",
        "/home/user/logs",
        "/home/user/.config/validator",
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} is missing."

def test_init_flag():
    flag_path = "/home/user/.config/validator/init.flag"
    assert os.path.isfile(flag_path), f"File {flag_path} is missing."
    with open(flag_path, "r") as f:
        content = f.read().strip()
    assert content == "READY", f"Expected {flag_path} to contain 'READY', but got '{content}'."

def test_operator_script_exists():
    script_path = "/home/user/operator.py"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    # Basic check to see if it's a valid python file (can be compiled)
    with open(script_path, "r") as f:
        source = f.read()
    try:
        compile(source, script_path, 'exec')
    except SyntaxError as e:
        assert False, f"{script_path} is not a valid Python script: {e}"

def test_run_system_sh_executable():
    script_path = "/home/user/run_system.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_active_symlinks_and_versions():
    active_dir = "/home/user/manifests/active"
    raw_dir = "/home/user/manifests/raw"
    versions_dir = "/home/user/manifests/versions"

    for app in ["app1.json", "app2.json"]:
        raw_path = os.path.join(raw_dir, app)
        active_path = os.path.join(active_dir, app)

        assert os.path.isfile(raw_path), f"Raw file {raw_path} is missing."
        assert os.path.islink(active_path), f"{active_path} is not a symlink."

        with open(raw_path, "rb") as f:
            content = f.read()
        md5_hash = hashlib.md5(content).hexdigest()

        app_name = os.path.splitext(app)[0]
        expected_version_file = f"{app_name}_{md5_hash}.json"
        expected_version_path = os.path.join(versions_dir, expected_version_file)

        assert os.path.isfile(expected_version_path), f"Versioned file {expected_version_path} is missing."

        target = os.readlink(active_path)
        assert os.path.abspath(os.path.join(active_dir, target)) == expected_version_path, \
            f"Symlink {active_path} does not point to {expected_version_path}."

def test_validation_report():
    report_path = "/home/user/logs/validation_report.txt"
    assert os.path.isfile(report_path), f"Validation report {report_path} is missing."
    with open(report_path, "r") as f:
        content = f.read().strip()
    expected = "VALIDATION_SUCCESS: All manifests are active and dependencies met."
    assert content == expected, f"Validation report content mismatch. Expected '{expected}', got '{content}'."

def test_crontab_installed():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        assert "run_system.sh" in result.stdout, "run_system.sh is not scheduled in the user crontab."
    except subprocess.CalledProcessError:
        assert False, "Failed to read crontab or crontab is empty."