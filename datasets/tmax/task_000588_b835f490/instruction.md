You are a container specialist tasked with configuring a local microservices environment for testing without root access. We need to set up process supervision for two microservices: a web frontend and a mock email relay.

Your task is to configure `supervisord` to manage these services, generate necessary TLS certificates, configure a non-root `nginx` instance, and start the system.

Here are the detailed requirements:

1. **Workspace setup**:
   All work must be done within `/home/user/microservices`.
   (Assume this directory exists, along with `/home/user/microservices/www` containing a sample `index.html`, and a mock email script at `/home/user/microservices/mailer.sh`).

2. **TLS Configuration**:
   Create a directory `/home/user/microservices/certs`.
   Generate a self-signed RSA 2048-bit certificate (`cert.pem`) and private key (`key.pem`) valid for 365 days in this directory. Do not use a passphrase. The subject details do not matter.

3. **Web Server Setup**:
   Create an Nginx configuration file at `/home/user/microservices/nginx.conf`.
   It must run as the current user, store its PID at `/home/user/microservices/nginx.pid`, and write access/error logs to `/home/user/microservices/nginx_access.log` and `/home/user/microservices/nginx_error.log`.
   Configure it to listen on port `8443` with SSL/TLS using the certificates generated in step 2.
   It should serve static files from `/home/user/microservices/www`.

4. **Process Supervision**:
   Create a supervisord configuration file at `/home/user/microservices/supervisord.conf`.
   Configure the `[supervisord]` section to write its log to `/home/user/microservices/supervisord.log` and its PID to `/home/user/microservices/supervisord.pid`.
   Configure two programs:
   - `webapp`: Runs `nginx -c /home/user/microservices/nginx.conf -g "daemon off;"`. Must auto-restart on unexpected failures.
   - `mailer`: Runs `bash /home/user/microservices/mailer.sh`. Must auto-restart on unexpected failures.

5. **Execution and Verification**:
   Start `supervisord` using your configuration file in the background.
   Once both services are running, run `supervisorctl -c /home/user/microservices/supervisord.conf status` and redirect the output to `/home/user/status.log`.