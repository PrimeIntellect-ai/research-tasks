You are an application system administrator. A recent deployment failed, and the user-level Nginx reverse proxy located at `http://127.0.0.1:8080/` is currently returning a `502 Bad Gateway` error. 

Your job is to debug and fix the deployment. 

The application ecosystem consists of:
1. An Nginx reverse proxy configured in `/home/user/nginx/nginx.conf`.
2. A Python web application located in `/home/user/app/`.
3. A custom mount configuration file `/home/user/fstab_config` intended to map data directories.

Perform the following tasks to fix the deployment:

1. **Fix the Nginx Configuration**:
   The Nginx configuration `/home/user/nginx/nginx.conf` has a misconfiguration causing the `502 Bad Gateway`. Identify the upstream port Nginx is trying to connect to, and modify the configuration to point to the correct application port, which is `8000`.

2. **Automate the Deployment with Python**:
   Create a Python script at `/home/user/deploy.py` that acts as the deployment automation tool. The script must do the following:
   - Read the `/home/user/fstab_config` file. This file mimics an `/etc/fstab` format. 
   - For any line containing the `bind` option (e.g., `/source /dest none bind 0 0`), the script must simulate the mount by creating a symbolic link at the destination path pointing to the source path. Ensure the parent directories for the destination exist.
   - Install the Python dependencies listed in `/home/user/app/requirements.txt` using `pip`.
   - Start the Python web application using `gunicorn --bind 127.0.0.1:8000 main:app` from within the `/home/user/app` directory as a background process.

3. **Deploy and Test**:
   - Stop Nginx if it is running, and restart it using the command: `nginx -c /home/user/nginx/nginx.conf -g "pid /home/user/nginx/nginx.pid;"`
   - Run your `/home/user/deploy.py` script to link the data and start the application.
   - Verify that `curl http://127.0.0.1:8080/data` successfully returns the contents of the mapped data directory. Write the output of this curl command to `/home/user/verification.log`.

Constraints:
- You must write the deployment script entirely in Python (`/home/user/deploy.py`).
- Do not use `sudo` or require root access.
- Ensure Gunicorn and Nginx remain running in the background after your tasks are complete.