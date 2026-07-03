# test_final_state.py
import os
import stat
import subprocess
import glob

def test_validator_exists_and_permissions():
    validator_path = "/home/user/validator"
    assert os.path.isfile(validator_path), f"{validator_path} does not exist."

    st = os.stat(validator_path)
    permissions = stat.S_IMODE(st.st_mode)
    expected_permissions = 0o711
    assert permissions == expected_permissions, f"Expected permissions 711 (octal), but got {oct(permissions)}."

def test_fw_config_script():
    fw_script_path = "/home/user/fw_config.sh"
    assert os.path.isfile(fw_script_path), f"{fw_script_path} does not exist."

    with open(fw_script_path, "r") as f:
        content = f.read()

    # Check for the required iptables components
    assert "iptables" in content, "iptables command not found in fw_config.sh."
    assert "-t nat" in content, "'-t nat' not found in fw_config.sh."
    assert "PREROUTING" in content, "'PREROUTING' not found in fw_config.sh."
    assert "80" in content, "Source port 80 not found in fw_config.sh."
    assert "8080" in content, "Destination port 8080 not found in fw_config.sh."

def test_adversarial_corpus_validator():
    validator_path = "/home/user/validator"
    clean_corpus_path = "/app/corpora/clean/"
    evil_corpus_path = "/app/corpora/evil/"

    # Ensure validator exists before testing
    assert os.path.isfile(validator_path), f"Validator binary {validator_path} is missing."

    clean_files = glob.glob(os.path.join(clean_corpus_path, "*.yaml")) + glob.glob(os.path.join(clean_corpus_path, "*.yml"))
    evil_files = glob.glob(os.path.join(evil_corpus_path, "*.yaml")) + glob.glob(os.path.join(evil_corpus_path, "*.yml"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_corpus_path}."
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_corpus_path}."

    failed_clean = []
    for fpath in clean_files:
        result = subprocess.run([validator_path, fpath], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(fpath))

    failed_evil = []
    for fpath in evil_files:
        result = subprocess.run([validator_path, fpath], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(fpath))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    assert not error_msgs, " | ".join(error_msgs)