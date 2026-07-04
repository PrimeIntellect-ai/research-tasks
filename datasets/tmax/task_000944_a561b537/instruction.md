I need you to act as our container deployment specialist. We are trying to roll out a local instance of our microservice, `py-state-manager`, but it keeps writing its state files to the wrong location (often causing permission denied errors or polluting the root filesystem) because of a path resolution bug in its vendored release. 

Here is what you need to do:

1. **Investigate the Vendored Package:**
   We have vendored the application source at `/app/vendored/py-state-manager-1.0.0`. It is a simple Python HTTP service that stores state files. There is a deliberate bug or misconfiguration in how it resolves its storage directory from the environment (it's supposed to read the `STORAGE_DIR` environment variable, but a typo or wrapper script issue overrides this with a bad relative path). Find and fix this perturbation so the application correctly respects the `STORAGE_DIR` environment variable.

2. **Write a Deployment Script:**
   Create a robust Python deployment script at `/home/user/deploy.py`. This script must:
   - Safely create the target directory `/home/user/app_data/storage` with `0755` permissions. Ensure robust error handling (e.g., if the directory already exists, handle it gracefully).
   - Start the fixed `py-state-manager` microservice in the background. 
   - The service must be configured via environment variables to listen on `127.0.0.1` port `9090`. (The app uses `HOST` and `PORT` environment variables).
   - Pass the authentication token to the service using the environment variable `AUTH_TOKEN=DeployMagic99`.
   - Set the `STORAGE_DIR` environment variable to `/home/user/app_data/storage`.

3. **Verify:**
   Ensure the service is actively running in the background and listening on port `9090` before your deployment script exits. The deployment script should return an exit code of `0` on success and print "Deployment successful" to standard output. Do not stop the service once started; it needs to remain running for our automated integration tests to interact with its HTTP API.