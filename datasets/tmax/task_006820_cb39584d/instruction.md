You are a security engineer tasked with rotating compromised credentials for an internal service. A recent automated vulnerability scan flagged that an active API token was leaked in the application's access logs. 

Your objectives are to find the leaked token, rotate it via the local authentication service, and test the new token using an isolated environment.

Here are the details:
1. **Find the leaked token:** 
   Analyze the log file located at `/home/user/app/logs/access.log`. Find the leaked 32-character alphanumeric API token (format: `Bearer <32-chars>`).

2. **Rotate the credential:**
   The authentication service is running locally at `http://127.0.0.1:9090`. 
   Generate a new 32-character lowercase hex token (e.g., using `openssl rand -hex 16`).
   Send a `POST` request to `http://127.0.0.1:9090/api/rotate`. The request must have a `Content-Type: application/json` header and a JSON payload containing both the old token and the new token:
   `{"old_token": "<the_leaked_token>", "new_token": "<your_new_token>"}`

3. **Test the authentication flow with process isolation:**
   Write a bash script at `/home/user/verify_auth.sh` that tests the new credential. To simulate process isolation and prevent the script from accidentally reading existing environment variables or the log file, the script MUST execute the `curl` test command using `env -i` (clearing all environment variables) and execute from `/tmp`.
   
   The `curl` command inside the script should send a `GET` request to `http://127.0.0.1:9090/api/verify` with the header `Authorization: Bearer <your_new_token>`.
   
   The script should write the exact HTTP response body received from the verify endpoint to `/home/user/verification_result.log`.

Make sure `/home/user/verify_auth.sh` is executable and run it so that `/home/user/verification_result.log` is generated.