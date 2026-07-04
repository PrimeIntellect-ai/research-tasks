You are a security engineer performing a credential rotation on a legacy internal Go application. The application source code is located at `/home/user/app/main.go`. 

Your objective is to test a known vulnerability to force a credential rotation, and then verify the rotation by analyzing the application's encrypted audit logs.

Here are the specific requirements:

1. **Vulnerability Analysis & Exploit Crafting:**
   - Review `/home/user/app/main.go`. The application uses a custom JWT implementation.
   - It has a documented endpoint `POST /admin/rotate` that accepts a JSON payload: `{"new_credential": "<your_new_key>"}`.
   - This endpoint requires an admin token, but the JWT parser is vulnerable. Craft a JWT that bypasses authentication (exploiting the JWT implementation) and elevates your privileges to the `"admin"` role.
   - Use the new credential value: `SECURE_ROTATED_CRED_2024`

2. **Execution:**
   - Start the Go application in the background (it listens on port 8080).
   - Send the exploit payload and the new credential to the `/admin/rotate` endpoint.

3. **Log Decryption & Parsing:**
   - Upon a successful rotation, the application writes an encrypted audit entry to `/home/user/app/audit.log`.
   - The encryption method and key are hardcoded in the application's source code.
   - Write a Go program at `/home/user/decrypt_log.go` that reads `/home/user/app/audit.log`, decrypts the payload, and extracts the generated `rotation_id` from the JSON log entry.

4. **Reporting:**
   - Create a final JSON report at `/home/user/result.json` with the following exact structure:
     ```json
     {
       "crafted_jwt": "<the exact JWT string you sent>",
       "rotation_id": "<the rotation_id extracted from the decrypted log>"
     }
     ```

Ensure your Go application is properly built and runs without errors. All required files should be exactly at the specified paths.