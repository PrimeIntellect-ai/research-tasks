You are an infrastructure engineer automating the provisioning of static assets using a local continuous deployment pipeline. Your goal is to create a robust, background Python service that mimics a deployment daemon, and a CI script that generates artifacts for it to process.

Perform the following tasks using Python (standard library only) and bash:

1. **Setup Directories**: 
   Create the following directories in `/home/user`:
   - `/home/user/ci_builds` (where new artifacts will be dropped)
   - `/home/user/active_deployment` (where the current active build is served from)

2. **Create the Deployment Daemon (`/home/user/watch_and_deploy.py`)**:
   Write a Python script that acts as a continuous running daemon. It should:
   - Run infinitely, checking the `/home/user/ci_builds/` directory every 2 seconds for any `.tar` files.
   - When a `.tar` file is detected:
     a. Clear all current contents of `/home/user/active_deployment/`.
     b. Extract the contents of the `.tar` file into `/home/user/active_deployment/`.
     c. Write a routing configuration file at `/home/user/deployment_network.conf` with exactly this format (replacing `<filename>` with the name of the processed tar file):
        ```
        ACTIVE_DIR=/home/user/active_deployment
        LAST_DEPLOYED=<filename>
        STATUS=live
        ```
     d. Delete the processed `.tar` file from `/home/user/ci_builds/` so it is not processed again.
   - You must run this script in the background and save its Process ID (PID) to `/home/user/watcher.pid`.

3. **Create the Mock CI Pipeline (`/home/user/mock_ci.py`)**:
   Write a second Python script that simulates a CI pipeline building and pushing artifacts. It should:
   - Create a file named `index.html` containing the text: `Build Version Alpha`.
   - Package this file into a tar archive named `build_alpha.tar`.
   - Move `build_alpha.tar` into `/home/user/ci_builds/`.
   - Pause for 4 seconds.
   - Create a new `index.html` containing the text: `Build Version Beta`.
   - Package this file into a tar archive named `build_beta.tar`.
   - Move `build_beta.tar` into `/home/user/ci_builds/`.
   
4. **Execution**:
   - Start your daemon (`watch_and_deploy.py`) in the background and ensure its PID is correctly written to the PID file.
   - Run `mock_ci.py` to trigger the pipeline.
   - Wait at least 5 seconds for the daemon to process the final artifact.

Ensure that by the end of the process, your daemon is still running (or verifiable via the PID file), `/home/user/active_deployment/index.html` contains "Build Version Beta", and `/home/user/deployment_network.conf` reflects `build_beta.tar` as the last deployed file.