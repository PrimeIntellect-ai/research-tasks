You are a security engineer tasked with securely rotating the credentials for a critical backend microservice. The internal secret vault has generated new credentials, but you must securely retrieve them, store them with proper access controls, and inject them into the microservice using strict process isolation to prevent environment leakage.

Here are your specific instructions:

1. **Secure Credential Retrieval (Certificate Chain Validation)**
   An internal vault server is running locally at `https://localhost:8443/secrets`. The server uses a certificate signed by an internal Certificate Authority (CA). The CA's public certificate is located at `/home/user/ca.crt`. 
   Write a Python script at `/home/user/fetch_secrets.py` that makes an HTTPS GET request to `https://localhost:8443/secrets`. Your script *must* explicitly validate the server's certificate chain using `/home/user/ca.crt`. (Do not disable SSL verification). The server will return a JSON object containing the new credentials.

2. **Access Control (File Permissions)**
   Save the JSON response from the vault server exactly as received into a file named `/home/user/prod_secrets.json`. To protect these credentials from unauthorized access, modify the permissions of `/home/user/prod_secrets.json` so that it is strictly read-only by the owner, and no one else has any permissions (i.e., `0400`).

3. **Process Isolation (Environment Sandboxing)**
   The microservice is located at `/home/user/app.py`. It requires the new credentials to be passed as environment variables named `DB_PASS` and `API_KEY`. However, `app.py` is a legacy script that aggressively logs its entire environment, which poses a security risk if standard environment variables (like user tokens, SSH keys, or paths) are present.
   Write a Bash wrapper script at `/home/user/run_app.sh` that:
   - Reads the values from `/home/user/prod_secrets.json`.
   - Executes `/home/user/app.py` in a completely cleared environment (using process isolation techniques like `env -i`).
   - Only passes exactly two environment variables to the app: `DB_PASS` and `API_KEY`. 

4. **Verification Log**
   When `/home/user/app.py` runs successfully with the correct environment variables and no extra leaked variables, it will print a unique success token to standard output. Capture this token and save it to a file named `/home/user/rotation_success.log`.

Ensure all file paths are exact and your final `rotation_success.log` contains only the token.