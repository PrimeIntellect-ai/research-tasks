# test_final_state.py
import os
import time
import subprocess

def test_deploy_and_service():
    deploy_script = "/home/user/deploy.sh"
    run_service_script = "/home/user/run_service.sh"

    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist"
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable"

    assert os.path.isfile(run_service_script), f"{run_service_script} does not exist"
    assert os.access(run_service_script, os.X_OK), f"{run_service_script} is not executable"

    # Run deploy.sh
    result = subprocess.run([deploy_script], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed with exit code {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"

    # Check if binary was copied
    assert os.path.isfile("/home/user/bin/user-mngr"), "/home/user/bin/user-mngr was not created by deploy.sh"
    assert os.access("/home/user/bin/user-mngr", os.X_OK), "/home/user/bin/user-mngr is not executable"

    # Wait briefly for service to start
    time.sleep(1)

    # Create request.txt
    queue_dir = "/home/user/queue"
    request_file = os.path.join(queue_dir, "request.txt")

    os.makedirs(queue_dir, exist_ok=True)
    with open(request_file, "w") as f:
        f.write("testuser1\ntestuser2\n")

    # Wait for the service to process the file (sleep 1 in loop + execution time)
    time.sleep(3)

    # Verify processing
    assert not os.path.exists(request_file), f"{request_file} was not deleted after processing"

    for u in ["testuser1", "testuser2"]:
        user_dir = f"/home/user/homes/{u}"
        assert os.path.isdir(user_dir), f"Directory {user_dir} was not created"

        readme_file = os.path.join(user_dir, "readme.txt")
        assert os.path.isfile(readme_file), f"File {readme_file} was not created"

        with open(readme_file, "r") as f:
            content = f.read().strip()

        assert content == f"Welcome {u}", f"Incorrect content in {readme_file}: expected 'Welcome {u}', got '{content}'"

    # Cleanup running supervisor to prevent dangling processes
    subprocess.run(["pkill", "-f", "run_service.sh"], capture_output=True)