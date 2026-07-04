As an incident responder, you are investigating a potentially compromised system. You need to secure exposed data, audit local services, and process encrypted logs left by an attacker. 

Perform the following tasks:

1. **Service Auditing**: A suspicious background HTTPS service is running on `localhost` on a port between `8400` and `8450`. Identify the exact port. Create the directory `/home/user/incident_report/` and save the port number (just the digits) into `/home/user/incident_report/suspicious_port.txt`.

2. **TLS/SSL Certificate Management**: The suspicious service uses a self-signed TLS certificate. Extract the public certificate from this running service and save it in PEM format to `/home/user/incident_report/extracted_cert.pem`.

3. **File Permissions**: The attacker left encrypted data files in `/home/user/incident_data/`. Some of these files have overly permissive access. Identify all `.dat` files in this directory that are readable, writable, or executable by "others" (the world). 
   - Change the permissions of these specific files to exactly `600` (read/write for owner only). 
   - Write the basenames (e.g., `file.dat`) of the files you *modified* into `/home/user/incident_report/secured_files.txt`, one per line, sorted alphabetically. Do not include files that were already secure.

4. **Data Processing (Python)**: There is a script at `/home/user/scripts/decrypt_data.py` designed to read the `.dat` files and fetch a decryption key from the suspicious local HTTPS service. However, it is currently failing due to SSL certificate verification errors.
   - Modify `/home/user/scripts/decrypt_data.py` so that it uses your extracted certificate (`/home/user/incident_report/extracted_cert.pem`) to securely verify the TLS connection. Do **not** simply disable SSL verification (e.g., do not use `verify=False`).
   - You will also need to update the port number in the script's URL to point to the correct discovered port.
   - Run the updated script. Upon success, it will process the logs and automatically output the results to `/home/user/incident_report/decrypted_intel.json`.

Ensure all requested files are exactly in the specified locations and formats.