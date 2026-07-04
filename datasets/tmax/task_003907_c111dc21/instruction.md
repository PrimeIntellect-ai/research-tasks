You are a backup operator responsible for verifying the integrity of restored configurations and CI/CD artifacts. A recent automated backup has been downloaded to `/home/user/backup.tar.gz`.

Your task is to write a robust Bash script at `/home/user/restore_tester.sh` that automates the extraction, processing, and verification of this backup. 

The script must perform the following actions:
1. Ensure robust error handling (e.g., fail fast on errors or unbound variables).
2. Extract `/home/user/backup.tar.gz` into a newly created directory `/home/user/restore_test/`.
3. Inside the extracted files, you will find `deploy_pipeline.log`. This file contains CI/CD deployment logs with UTC timestamps. Find the timestamp of the *latest* (chronologically most recent) deployment that has the string `STATUS: SUCCESS`.
4. Convert this UTC timestamp into the `Asia/Tokyo` timezone. Format the converted time exactly as `YYYY-MM-DD HH:MM:SS`.
5. You will also find a reverse proxy configuration template named `proxy_template.conf`. To test this locally without root privileges, use text processing tools to modify the configuration:
   - Change any `listen 80;` directives to `listen 8080;`
   - Change any `listen 443;` directives to `listen 8443;`
   - Save the modified configuration to `/home/user/restore_test/local_proxy.conf`.
6. Finally, generate a verification report in JSON format at `/home/user/restore_report.json`. The JSON must have exactly this structure:

```json
{
  "last_successful_deploy_tokyo": "YYYY-MM-DD HH:MM:SS",
  "proxy_listen_ports": [
    "8080",
    "8443"
  ]
}
```
*Note: Extract the actual modified port numbers from `local_proxy.conf` to populate the `proxy_listen_ports` array, ensuring your text processing worked.*

Ensure your script is executable (`chmod +x /home/user/restore_tester.sh`) and can be run without any arguments. Do not run the script yourself; the automated testing suite will execute your script and verify the resulting `/home/user/restore_report.json` and `/home/user/restore_test/local_proxy.conf` files.