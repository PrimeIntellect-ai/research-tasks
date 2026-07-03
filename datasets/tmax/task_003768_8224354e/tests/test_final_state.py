# test_final_state.py

import os
import subprocess
import stat

def test_analyzer_compiled():
    analyzer_exe = "/home/user/analyzer"
    assert os.path.isfile(analyzer_exe), f"Analyzer executable not found at {analyzer_exe}"
    assert os.access(analyzer_exe, os.X_OK), f"Analyzer is not executable: {analyzer_exe}"

    # Check if it's an ELF file
    with open(analyzer_exe, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{analyzer_exe} is not a valid ELF executable"

def test_start_service_script():
    script_path = "/home/user/start_service.sh"
    assert os.path.isfile(script_path), f"Service script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Service script is not executable: {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "cloud_repo" in content, "Script does not check for cloud_repo"
    assert "tar" in content, "Script does not contain tar extraction command"
    assert "exit 2" in content or "exit  2" in content, "Script does not exit with code 2 on tar failure"
    assert "/home/user/analyzer" in content, "Script does not execute the analyzer"

def test_cloud_repo_restored_and_updated():
    repo_path = "/home/user/cloud_repo"
    assert os.path.isdir(repo_path), f"Repository directory not found at {repo_path}"
    assert os.path.isdir(os.path.join(repo_path, ".git")), f"Not a valid git repository: {repo_path}"

    new_resource = os.path.join(repo_path, "new_resource.json")
    assert os.path.isfile(new_resource), f"new_resource.json not found in {repo_path}"

    # Check if new_resource.json is tracked by git
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "new_resource.json"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, "new_resource.json is not tracked by git"

    # Check commit message
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        text=True
    )
    assert "Add new resource" in result.stdout, "Latest commit does not have the expected message"

def test_git_hook():
    hook_path = "/home/user/cloud_repo/.git/hooks/post-commit"
    assert os.path.isfile(hook_path), f"Git hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook is not executable: {hook_path}"

    with open(hook_path, "r") as f:
        content = f.read()

    assert "HOOK_FIRED" in content, "Git hook does not contain the text 'HOOK_FIRED'"
    assert "/home/user/analyzer" in content, "Git hook does not execute the analyzer"

def test_hook_log():
    log_path = "/home/user/hook_log.txt"
    assert os.path.isfile(log_path), f"Hook log file not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "HOOK_FIRED" in content, "Hook log does not contain 'HOOK_FIRED'"

def test_cost_report():
    report_path = "/home/user/cost_report.txt"
    assert os.path.isfile(report_path), f"Cost report not found at {report_path}"

    with open(report_path, "r") as f:
        content = f.read()

    assert "ANALYSIS_COMPLETE" in content, "Cost report does not contain 'ANALYSIS_COMPLETE'"