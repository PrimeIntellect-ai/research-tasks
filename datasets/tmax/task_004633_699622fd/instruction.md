You are an administrator managing an internal system that tracks user mailing list subscriptions. 

Currently, there is a background process script located at `/home/user/monitor.py` which scans the directory `/home/user/mailing_lists/` for user configuration files (ending in `.list_config`). It aggregates the emails found in these files and outputs them to `/home/user/status.json`.

However, the system is malfunctioning. Users are complaining that their subscriptions are not appearing in the output. The `monitor.py` script has a strict security requirement: similar to SSH private keys, it silently ignores any `.list_config` file that is accessible to anyone other than the owner.

Your task is to:
1. Identify and fix the filesystem permission issues in `/home/user/mailing_lists/` so that all user configuration files are securely processed by the monitor. The files must be readable and writable *only* by the owner.
2. Create a directory `/home/user/certs/` and generate a self-signed TLS certificate (`cert.pem`) and private key (`key.pem`) without a passphrase.
3. Write a Python script at `/home/user/server.py` that serves the contents of `/home/user/status.json` on port `8443` over HTTPS. The server must use Python's built-in `http.server` and `ssl` modules, and it should return the JSON file when an HTTPS GET request is made to the root path (`/status.json`).
4. Start both `/home/user/monitor.py` and `/home/user/server.py` as background processes and ensure they stay running.

At the end of your task:
- All files in `/home/user/mailing_lists/` must have the correct permissions.
- `/home/user/status.json` must exist and contain the data for all users.
- `/home/user/server.py` must be running and serving HTTPS traffic on port 8443.

Ensure both scripts are running continuously in the background before you finish.