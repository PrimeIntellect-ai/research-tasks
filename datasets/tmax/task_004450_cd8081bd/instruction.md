You are a backup operator testing a deployment restore procedure on a staging environment. You must restore an application's directory structure, identify storage-heavy files, configure basic access credentials, and write a simple Bash-based traffic forwarder to simulate a reverse proxy. 

Perform the following tasks using Bash and standard Linux command-line tools. You do not have root access.

1. **Deployment Restore & Link Management**:
   A backup archive is located at `/home/user/backup.tar.gz`. 
   - Extract this archive into `/home/user/deployments/`.
   - The archive contains two directories: `app-v1` and `app-v2`. Create a symbolic link at `/home/user/deployments/live` that points to the `/home/user/deployments/app-v2` directory.

2. **Storage Monitoring**:
   - As part of our quota monitoring, find all files within `/home/user/deployments/` (including all subdirectories) that are strictly larger than 100 Kilobytes.
   - Write the absolute paths of these files to `/home/user/large_files.log`, one path per line.

3. **User Access Administration**:
   - The proxy you will set up requires basic authentication credentials. Generate an htpasswd-compatible file at `/home/user/proxy_users.txt`.
   - Add a single user named `backup_admin` with the password `staging_pass_2024`. Use `openssl passwd -apr1` or `htpasswd` to securely hash the password (MD5-based Apache format).

4. **Bash Reverse Proxy Setup**:
   - Write a Bash script at `/home/user/start_proxy.sh` that simulates a reverse proxy. 
   - The script must use `socat`, `nc`, or `ncat` to listen on TCP port `8080` and forward all incoming traffic to `localhost:9090` (where the mock backend application would be running).
   - The script should run continuously to handle multiple connections if possible (e.g., using a `while` loop or native `keep-alive` flags like `ncat -k`).
   - Ensure the script is executable (`chmod +x`).

Do not start the proxy script; just write it and ensure it is executable. Ensure all file paths and outputs match the requirements exactly.