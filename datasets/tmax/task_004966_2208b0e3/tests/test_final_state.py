# test_final_state.py
import os

def test_symlink_exists_and_correct():
    symlink_path = "/home/user/operator-data/inputs/legacy"
    target_path = "/home/user/legacy-manifests"

    assert os.path.islink(symlink_path), f"Expected '{symlink_path}' to be a symlink. It is missing or not a symlink."
    actual_target = os.readlink(symlink_path)
    assert actual_target == target_path, f"Symlink '{symlink_path}' points to '{actual_target}', expected '{target_path}'."

def test_compiled_yaml_exists_and_contains_manifests():
    compiled_path = "/home/user/operator-data/outputs/compiled.yaml"
    assert os.path.isfile(compiled_path), f"File '{compiled_path}' does not exist. The operator script may have failed or was not configured correctly."

    with open(compiled_path, "r") as f:
        content = f.read()

    assert "name: app1" in content, f"'{compiled_path}' does not contain the expected app1 manifest content. Check your directory structure and symlink."

def test_operator_log_exists_and_contains_output():
    log_path = "/home/user/operator-data/operator.log"
    assert os.path.isfile(log_path), f"File '{log_path}' does not exist. Ensure the operator script ran successfully."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Applying manifests" in content, f"'{log_path}' is missing the expected dummy kubectl output. Ensure the PATH was updated correctly in the profile."

def test_status_log_exists_and_contains_metrics_status():
    status_path = "/home/user/operator-data/outputs/status.log"
    assert os.path.isfile(status_path), f"File '{status_path}' does not exist. Ensure check_metrics.sh was created and executed."

    with open(status_path, "r") as f:
        content = f.read()

    assert "METRICS_UP=1" in content, f"'{status_path}' does not contain 'METRICS_UP=1'. Check the logic in check_metrics.sh."