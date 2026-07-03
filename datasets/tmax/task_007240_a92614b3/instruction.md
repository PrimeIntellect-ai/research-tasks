You are tasked with fixing and automating a local deployment pipeline for a Python microservice, managed by `supervisord`. You must perform this without root access.

Currently, we have a basic web application (`webapp`) and an accompanying monitoring agent (`metrics`). 
There are two main issues:
1. The deployment process is manual.
2. The `metrics` service fails to start because it depends on `webapp` being fully initialized, but `webapp` has a simulated 2-second startup delay. Since `metrics` immediately tries to connect and fails, `supervisord` marks it as FATAL.

Your objectives:

1. **Configure Git Hooks**: 
   A bare repository exists at `/home/user/api.git`.
   Create an executable `post-receive` hook at `/home/user/api.git/hooks/post-receive`. 
   When code is pushed to this repository, the hook must:
   - Check out the code to the working directory `/home/user/api_app`. (Hint: Use `GIT_WORK_TREE=/home/user/api_app git checkout -f`).
   - Run `supervisorctl -c /home/user/supervisord.conf restart all` to restart the services.

2. **Fix the Missing Dependency Issue**:
   The source code for the services is currently located in a local clone at `/home/user/local_clone`.
   The `metrics.py` script attempts to hit `http://localhost:8080` exactly once and crashes if it fails.
   Modify `/home/user/local_clone/metrics.py` using Python so that it implements a retry mechanism. It should try to connect up to 5 times, sleeping for 1 second between attempts, before crashing.

3. **Deploy & Verify**:
   - Start the process supervisor in the background using `supervisord -c /home/user/supervisord.conf`.
   - Commit your modifications to `metrics.py` in the `/home/user/local_clone` repository.
   - Push the changes to the bare remote repository (`origin main`).
   - Redirect the standard output and standard error of the `git push` command to `/home/user/push_output.log`.
   
After you finish, both `webapp` and `metrics` must be in the `RUNNING` state when checking `supervisorctl -c /home/user/supervisord.conf status`.