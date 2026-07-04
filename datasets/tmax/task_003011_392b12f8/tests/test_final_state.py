# test_final_state.py
import os
import sys
import glob
import subprocess

def test_vendored_package_fixed():
    """Check that the deliberate bug in the vendored package is fixed."""
    sys.path.insert(0, "/app/vendored/qemu-net-builder")
    try:
        from qemu_net_builder.utils import get_subnet
        subnet = get_subnet()
        assert isinstance(subnet, str), f"get_subnet() returned {type(subnet)}, expected str"
    except TypeError as e:
        assert False, f"get_subnet() still raises a TypeError: {e}"
    except ImportError as e:
        assert False, f"Failed to import qemu_net_builder.utils: {e}"
    finally:
        sys.path.pop(0)

def test_validate_configs_clean_corpus():
    """Check that the validation script accepts all clean configurations."""
    script_path = "/home/user/validate_configs.py"
    assert os.path.isfile(script_path), f"Validation script {script_path} not found."

    clean_files = glob.glob("/home/user/corpora/clean/*.json")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        result = subprocess.run(["/usr/bin/python3", script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_validate_configs_evil_corpus():
    """Check that the validation script rejects all malicious configurations."""
    script_path = "/home/user/validate_configs.py"
    assert os.path.isfile(script_path), f"Validation script {script_path} not found."

    evil_files = glob.glob("/home/user/corpora/evil/*.json")
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_files = []
    for f in evil_files:
        result = subprocess.run(["/usr/bin/python3", script_path, f], capture_output=True)
        if result.returncode != 1:
            bypassed_files.append(os.path.basename(f))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"

def test_systemd_service_file():
    """Check that the systemd service file is created correctly."""
    service_file = "/home/user/.config/systemd/user/qemu-net-validator.service"
    assert os.path.isfile(service_file), f"Systemd service file {service_file} is missing."

    with open(service_file, "r") as f:
        content = f.read()

    expected_desc = "Description=QEMU Net Validator"
    expected_exec = "ExecStart=/usr/bin/python3 /home/user/validate_configs.py /home/user/default_config.json"
    expected_restart = "Restart=on-failure"

    assert expected_desc in content, f"'{expected_desc}' not found in service file."
    assert expected_exec in content, f"'{expected_exec}' not found in service file."
    assert expected_restart in content, f"'{expected_restart}' not found in service file."