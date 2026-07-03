You are tasked with organizing and securing a multi-language project's files before configuring its CI/CD pipeline. The project is located at `/home/user/project`.

Please complete the following steps to secure the repository:

1. **Structured Data Parsing & Transformation**: 
   There is a configuration file at `/home/user/project/config.json`. Using standard bash tools (e.g., `jq`), parse this file and transform it by replacing the values of the `api_key` and `password` keys (located inside the `credentials` object) with the exact string `***MASKED***`. Leave all other keys and structure intact. Save the resulting JSON to `/home/user/project/config_secure.json`.

2. **Patch Processing**: 
   A security patch has been provided at `/home/user/project/security.patch` to mitigate a vulnerability in the Node.js server. Apply this patch to the target file. (The patch was generated relative to the `/home/user/project` directory).

3. **CI/CD Pipeline Setup**: 
   Write a shell script at `/home/user/project/ci_check.sh` that will serve as a continuous integration security check. 
   - The script must recursively search for the exact string `SECRET_` in all files within the `/home/user/project/src/` directory.
   - If the string is found anywhere, the script must exit with a status code of `1`.
   - If the string is not found, it must exit with a status code of `0`.
   - Ensure the script has executable permissions (`chmod +x`).

4. **Remediation**: 
   There is currently a file in `/home/user/project/src/` that contains a leaked secret (the string `SECRET_`). Identify this file and completely delete it from the directory.

5. **Logging**: 
   Create a file at `/home/user/project/deleted_file.log` and write exactly the base name of the file you deleted in Step 4 (e.g., if you deleted `/home/user/project/src/bad_file.txt`, write `bad_file.txt` into the log).

Make sure all outputs are exactly as specified so the automated tests can verify your work.