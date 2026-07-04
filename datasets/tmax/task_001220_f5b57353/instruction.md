You are an operations engineer testing our automated backup restoration and staged deployment process. We have a multi-service mock environment running locally to test your code. 

Currently, the following services are running in the background:
1. An HTTP Server on `127.0.0.1:8080` that serves backup archives.
2. A local SMTP sink on `127.0.0.1:2525`.

Your task is to write a C++ daemon (`/home/user/restorer.cpp`) and compile it to `/home/user/restorer`. 

This daemon must coordinate a rolling restore deployment by implementing the following:
1. **Listen for Commands:** The C++ daemon must start a TCP server listening on `127.0.0.1:9090`.
2. **Handle Restores:** When a client connects and sends the string `RESTORE <version>\n` (e.g., `RESTORE v2.1\n`), the daemon must perform the following staged deployment:
   - **Download:** Fetch the backup archive from `http://127.0.0.1:8080/backups/<version>.tar.gz` and save it to `/home/user/staging.tar.gz`. (You may invoke shell tools like `curl` and `tar` from C++).
   - **Extract:** Extract the contents into `/home/user/restore_deploy/` (create this directory if it doesn't exist).
   - **Permissions (ACL equivalent):** The archive contains two files: `app.bin` and `config.json`. You must enforce strict permissions: `/home/user/restore_deploy/app.bin` must be set to `0750` and `/home/user/restore_deploy/config.json` must be set to `0600`.
   - **Notify via SMTP:** Open a raw TCP socket to the SMTP server at `127.0.0.1:2525` and send a standard SMTP payload to deliver an email.
     - MAIL FROM: `<system@local.test>`
     - RCPT TO: `<operator@backup.local>`
     - Subject: `Restore <version> complete`
   - **Acknowledge:** After successfully completing the above, send `SUCCESS\n` back to the TCP client and gracefully close the client connection. The server should remain running to accept future connections.

**Rules & Constraints:**
- Compile the program using `g++ -std=c++11 /home/user/restorer.cpp -o /home/user/restorer`.
- Leave the compiled `/home/user/restorer` running in the background so our verification suite can test it.
- All file paths must be exact.
- Ensure proper error checking so the daemon doesn't crash on invalid inputs.