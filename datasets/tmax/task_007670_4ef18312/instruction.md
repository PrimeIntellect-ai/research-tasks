You are a Linux systems engineer tasked with hardening and fixing a local development environment. 

A developer has set up an Nginx reverse proxy to front a Python-based web application, but they are receiving a 502 Bad Gateway error when trying to access the site on `http://localhost:8080`.

Here is the current state of the system:
- The Python application is located at `/home/user/app/server.py`. When run, it listens on a UNIX socket located at `/home/user/app/app.sock`.
- The locally installed Nginx configuration is located at `/home/user/nginx/nginx.conf`. It is configured to run entirely in user-space without root privileges.
- Nginx is supposed to proxy requests from port 8080 to the Python application's UNIX socket.

Your tasks are to:
1. Identify and fix the misconfiguration in `/home/user/nginx/nginx.conf` causing the 502 error (Hint: inspect the upstream socket path).
2. Start the Python backend application in the background (`python3 /home/user/app/server.py &`).
3. Start Nginx using the local configuration (`nginx -c /home/user/nginx/nginx.conf &`).
4. Ensure that `curl http://localhost:8080` successfully returns the application's response ("Hello World").
5. Write a Python script at `/home/user/backup.py` that performs a backup of the fixed Nginx configuration file. The script must read `/home/user/nginx/nginx.conf`, copy its contents to `/home/user/backup/nginx.conf.bak`, and append exactly this string as a new line at the very end of the backup file: `# BACKUP SUCCESSFUL`. Run this script once.

Ensure everything is running and the backup file is created correctly before completing the task.