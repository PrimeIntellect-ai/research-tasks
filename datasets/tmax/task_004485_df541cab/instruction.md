You are an infrastructure engineer tasked with automating the provisioning of a legacy application that lacks modern configuration management capabilities. The application setup is strictly interactive, and you need to build a mini CI/CD pipeline to automate its configuration and lifecycle deployment.

All your work should be done in `/home/user/ci_pipeline/`.

Here is the current system state:
- There is a mock interactive setup script located at `/home/user/legacy_service/setup.sh`.
- There is a mock service daemon located at `/home/user/legacy_service/daemon.py`.

Your objective is to complete the following phases:

**Phase 1: Python Expect Scripting**
Create a Python script at `/home/user/ci_pipeline/automate_setup.py` that uses the `pexpect` library to interact with `/home/user/legacy_service/setup.sh`. 
You must programmatically answer the interactive prompts with the following exact values:
- Admin Username: `ci_admin`
- Admin Password: `ci_supersecret`
- Service Port: `8080`
- Configuration Token: `TOKEN_842X`

**Phase 2: CI/CD Pipeline Construction & Lifecycle Management**
Create a Bash script at `/home/user/ci_pipeline/run_pipeline.sh` that automates the deployment process. This script must:
1. Create a Python virtual environment at `/home/user/ci_pipeline/venv`.
2. Activate the virtual environment and install `pexpect`.
3. Execute your `/home/user/ci_pipeline/automate_setup.py` script to provision the legacy service.
4. Start the service daemon (`/home/user/legacy_service/daemon.py`) in the background.
5. Save the Process ID (PID) of the background daemon into `/home/user/ci_pipeline/service.pid`.
6. Wait 3 seconds to ensure the service has fully started.
7. Use `curl` to send a GET request to `http://127.0.0.1:8080/health` and save the exact standard output to `/home/user/ci_pipeline/health_check.log`.

Make sure `/home/user/ci_pipeline/run_pipeline.sh` is executable and run it to complete the provisioning pipeline. Keep the daemon running in the background when you are finished.