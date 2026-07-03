You are a site administrator managing a local CI/CD setup for a user account management system. 

A deployment pipeline for a microservice architecture is failing due to a combination of missing storage checks, a broken Git hook, and a network misconfiguration between the services. 

Your objective is to fix the environment in `/home/user/app_repo` so that the test pipeline passes and changes can be committed.

Perform the following tasks:

1. **Storage Monitoring Script**: 
   Create a bash script at `/home/user/app_repo/check_quota.sh`. The script must check the file size in bytes of `/home/user/app_repo/users.db`. 
   - If the file size is greater than 1024 bytes, the script must print "QUOTA_EXCEEDED" to standard output and exit with status code 1.
   - If the file size is 1024 bytes or less, it must print "QUOTA_OK" and exit with status code 0.
   - Make sure the script is executable.

2. **Fix the Network Misconfiguration**: 
   The application consists of two services: `api.py` and `auth.py`. 
   - `auth.py` binds to a specific port defined internally.
   - `api.py` reads `/home/user/app_repo/config.json` to know which port to connect to for authentication. 
   Currently, `api.py` crashes because it tries to reach `auth.py` on the wrong port. Inspect the Python files and the JSON config, identify the port `auth.py` actually listens on, and fix `/home/user/app_repo/config.json` so that `api.py` can successfully fetch data from `auth.py`.

3. **Configure the Git Hook (CI/CD Pipeline)**:
   Create a Git hook at `/home/user/app_repo/.git/hooks/pre-commit` (ensure it is executable). The hook must do exactly the following in order:
   - Execute `./check_quota.sh`. If it fails (non-zero exit), the commit must be aborted.
   - Execute `python3 run_tests.py`. If it fails, the commit must be aborted. 

4. **Trigger the Pipeline**:
   Stage your modified files (`check_quota.sh`, `config.json`, etc.) and commit them to the local repository at `/home/user/app_repo` with the commit message `Fix pipeline`. 
   
If everything is configured correctly, the `pre-commit` hook will run the tests. `run_tests.py` will spin up the services, verify they can communicate, and write a final verification file to `/home/user/test_results.log` containing `PIPELINE_PASSED`.