# test_final_state.py
import os
import stat
import subprocess
import re

def test_systemd_service_dependency():
    operator_path = "/home/user/.config/systemd/user/manifest-operator.service"
    assert os.path.isfile(operator_path), f"Missing {operator_path}"

    with open(operator_path, "r") as f:
        content = f.read()

    assert re.search(r"After=.*k8s-mock-api\.service", content), "manifest-operator.service is missing After=k8s-mock-api.service"
    assert re.search(r"(Requires|Wants)=.*k8s-mock-api\.service", content), "manifest-operator.service is missing Requires=k8s-mock-api.service"

def test_git_hook_and_expect_script():
    workspace_repo = "/home/user/workspace/k8s-manifests"
    expect_script = "/home/user/auto-push.exp"
    hook_log = "/home/user/operator-logs/hook.log"

    assert os.path.isfile(expect_script), f"Missing expect script at {expect_script}"
    st = os.stat(expect_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"{expect_script} is not executable"

    # Make a commit to test the hook and auto-push
    config_file = os.path.join(workspace_repo, "config.yaml")
    with open(config_file, "a") as f:
        f.write("\n# update\n")

    subprocess.run(["git", "commit", "-am", "update"], cwd=workspace_repo, check=True)

    # Run the expect script
    result = subprocess.run([expect_script], cwd=workspace_repo, capture_output=True, text=True)
    assert result.returncode == 0, f"Expect script failed with return code {result.returncode}\nOutput: {result.stdout}\nError: {result.stderr}"

    # Get the new commit hash
    rev_parse = subprocess.run(["git", "rev-parse", "HEAD"], cwd=workspace_repo, capture_output=True, text=True, check=True)
    newrev = rev_parse.stdout.strip()

    # Check the hook log
    assert os.path.isfile(hook_log), f"Missing hook log at {hook_log}"
    with open(hook_log, "r") as f:
        log_content = f.read()

    expected_log = f"HOOK_TRIGGERED: {newrev}"
    assert expected_log in log_content, f"Hook log does not contain expected string '{expected_log}'"

def test_logrotate_config():
    logrotate_conf = "/home/user/logrotate.conf"
    assert os.path.isfile(logrotate_conf), f"Missing {logrotate_conf}"

    with open(logrotate_conf, "r") as f:
        content = f.read()

    assert "/home/user/operator-logs/*.log" in content, f"Logrotate config does not target /home/user/operator-logs/*.log"
    assert "daily" in content, "Logrotate config missing 'daily'"
    assert re.search(r"rotate\s+3", content), "Logrotate config missing 'rotate 3'"
    assert "compress" in content, "Logrotate config missing 'compress'"