You are a cloud architect migrating an internal authentication proxy service to a new staging environment. The source code for the proxy service is provided as a vendored package, but it has not been fully adapted to the new environment and contains a bug. Your goal is to fix the package, automate its deployment using idempotent scripts, and ensure the service is running correctly.

Perform the following tasks:

1. **Fix the Vendored Package:**
   The source code for the service is located at `/app/auth_proxy-1.2.3`. During the migration, a bug was introduced in the HTTP header parsing logic inside the package (specifically in how it reads the authorization token from incoming requests). Inspect the source code, identify the typo or logic error related to the Authorization header, and fix it. The service expects standard `Authorization: Bearer <token>` headers.

2. **User Account Administration & Deployment Setup:**
   The service requires a JSON configuration file to map authentication tokens to users and groups. 
   Write an idempotent bash script at `/home/user/deploy.sh` that performs the following steps:
   - Safely terminates any existing instance of the `auth-proxy` service.
   - Generates the configuration file at `/home/user/users.json` containing exactly these users:
     ```json
     {
       "users": [
         {"username": "admin", "token": "super-secret-99", "group": "sysadmin"},
         {"username": "guest", "token": "guest-token-11", "group": "readonly"}
       ]
     }
     ```
   - Creates a Python virtual environment at `/home/user/venv`.
   - Installs the fixed `auth_proxy` package from `/app/auth_proxy-1.2.3` into this virtual environment.
   - Starts the `auth-proxy` service in the background. The service should be invoked via the virtual environment's bin directory, passing the arguments: `--config /home/user/users.json --port 9090 --host 127.0.0.1`.

3. **Connectivity Diagnostics:**
   Write a diagnostic shell script at `/home/user/check_health.sh` that uses `curl` to test the service. It should make an HTTP GET request to `http://127.0.0.1:9090/api/whoami` using the admin token (`super-secret-99`) as a Bearer token, and print the output. 

4. **Execution:**
   Run your `/home/user/deploy.sh` script so that the virtual environment is built, the package is installed, and the service is actively listening on port 9090.

Ensure your deployment script is fully idempotent (it can be run multiple times without failing or leaving orphaned background processes). Do not use root privileges.