You are troubleshooting a custom email gateway on a Linux server. The system consists of three components:
1. An Nginx reverse proxy listening on port 8080.
2. A backend service (using socat and an Expect script) that accepts requests via a Unix domain socket, processes them, and sends emails via a local SMTP server.
3. A local mock SMTP server listening on port 2525.

Currently, if you make a request to the web server (e.g., `curl http://127.0.0.1:8080/send`), it returns a "502 Bad Gateway" error. 

Your task is to fix the system so that an automated end-to-end test can successfully trigger an email. You need to accomplish the following:

1. **Fix the Nginx Configuration**: The Nginx configuration file is located at `/home/user/app/nginx/nginx.conf`. It is currently pointing to the wrong upstream socket path. The backend actually listens on `/home/user/app/private/api.sock`. Update the Nginx configuration to point to the correct socket. Nginx must be restarted or reloaded afterward.
2. **Configure ACLs**: The automated verifier will connect to the socket directly as the user `guest` to bypass Nginx during some tests. Currently, the `guest` user cannot access the socket due to restrictive permissions on the directory and socket. Use `setfacl` to grant the user `guest` read and write (`rw`) access to `/home/user/app/private/api.sock` and execute (`x`) access to the `/home/user/app/private` directory.
3. **Write the Subject Sanitizer (C Program)**: The Expect script relies on a C program located at `/home/user/app/sanitize_subject` to clean up the HTTP request body before using it as the email subject. The source file should be written to `/home/user/app/sanitize_subject.c` and compiled to `/home/user/app/sanitize_subject`.
   - The program must read an arbitrary sequence of bytes from `stdin` until EOF.
   - For each character read:
     - If it is an alphanumeric character (a-z, A-Z, 0-9) or a space (' '), convert it to uppercase and print it to `stdout`.
     - If it is any other character (including newlines, punctuation, or non-printable characters), silently discard it.
   - The program must exit with status code 0.
   
Ensure that the final end-to-end flow works: Nginx must correctly proxy requests to the backend socket, the backend must use your C program to sanitize the subject, and the Expect script must successfully negotiate the SMTP transaction.