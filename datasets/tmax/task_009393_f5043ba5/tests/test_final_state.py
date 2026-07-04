# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import re

def test_directories_exist():
    assert os.path.isdir("/home/user/spool"), "Directory /home/user/spool does not exist"
    assert os.path.isdir("/home/user/results"), "Directory /home/user/results does not exist"

def test_git_repo_and_hook():
    repo_dir = "/home/user/backup_repo.git"
    assert os.path.isdir(os.path.join(repo_dir, "objects")), f"Bare git repository not found at {repo_dir}"

    hook_path = os.path.join(repo_dir, "hooks", "post-receive")
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook at {hook_path} is not executable"

def test_verify_restore_program():
    prog_path = "/home/user/verify_restore"
    assert os.path.isfile(prog_path), f"C++ program not found at {prog_path}"
    assert os.access(prog_path, os.X_OK), f"C++ program at {prog_path} is not executable"

    # Test OK case
    p = subprocess.run([prog_path], input=b"file1.dat\nfile2.dat\n", capture_output=True)
    assert p.stdout.decode('utf-8').strip() == "STATUS: OK, COUNT: 2", "verify_restore did not output 'STATUS: OK, COUNT: 2' for valid input"

    # Test ERROR case
    p = subprocess.run([prog_path], input=b"file1.dat\nbadfile.txt\nfile3.dat\n", capture_output=True)
    assert p.stdout.decode('utf-8').strip() == "STATUS: ERROR", "verify_restore did not output 'STATUS: ERROR' for invalid input"

    # Test EMPTY case
    p = subprocess.run([prog_path], input=b"", capture_output=True)
    assert p.stdout.decode('utf-8').strip() == "STATUS: EMPTY", "verify_restore did not output 'STATUS: EMPTY' for empty input"

def test_cron_configuration():
    cron_path = "/home/user/backup_cron.txt"
    assert os.path.isfile(cron_path), f"Cron file not found at {cron_path}"
    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Check for valid cron schedule
    assert re.search(r'^\s*\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/run_tests\.sh\s*$', content, re.MULTILINE), \
        f"Cron configuration in {cron_path} is incorrect. Expected '*/5 * * * * /home/user/run_tests.sh'"

def test_pipeline_execution():
    script_path = "/home/user/run_tests.sh"
    assert os.path.isfile(script_path), f"Processing script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Processing script at {script_path} is not executable"

    # Create a temporary clone to push from
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["git", "clone", "/home/user/backup_repo.git", tmpdir], check=True, capture_output=True)

        # Create restore.log
        log_content = "INFO starting\nRESTORED data1.dat\nIGNORED config.cfg\nRESTORED data2.dat\n"
        with open(os.path.join(tmpdir, "restore.log"), "w") as f:
            f.write(log_content)

        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "add", "restore.log"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Add restore.log"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, check=True, capture_output=True)

        p_rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmpdir, check=True, capture_output=True)
        newrev = p_rev.stdout.decode('utf-8').strip()

    # The post-receive hook should have created a job file
    job_file = f"/home/user/spool/{newrev}.job"
    assert os.path.isfile(job_file), f"Job file {job_file} was not created by the post-receive hook"

    # Run the processing script
    subprocess.run([script_path], check=True, capture_output=True)

    # Check results
    out_file = f"/home/user/results/{newrev}.out"
    assert os.path.isfile(out_file), f"Result file {out_file} was not created by the processing script"

    with open(out_file, 'r') as f:
        result = f.read().strip()

    assert result == "STATUS: OK, COUNT: 2", f"Result file {out_file} contained '{result}', expected 'STATUS: OK, COUNT: 2'"
    assert not os.path.exists(job_file), f"Job file {job_file} was not deleted after processing"