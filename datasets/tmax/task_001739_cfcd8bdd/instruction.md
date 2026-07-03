You are a Linux systems engineer responsible for hardening our infrastructure. We have a custom, minimal web server written in C that handles static file serving. The source code for this server is vendored at `/app/tinyweb-1.0.0`. 

Your objective is to fix a bug in the vendored package, secure its deployment, and write an idempotent setup script.

Here are the specific requirements:

1. **Vendored Package Fix**: The package at `/app/tinyweb-1.0.0` has a broken `Makefile` and a missing environment variable check in `server.c` that causes it to crash when TLS is enabled. Fix the `Makefile` so it links against OpenSSL properly (`-lssl -lcrypto`), and fix `server.c` to gracefully handle the absence of the `TLS_CERT_PATH` environment variable by falling back to `/etc/tinyweb/cert.pem`. Compile the fixed server.

2. **User and Group Setup**: Create a system group named `webfiles` and a user named `tinyweb_usr`. The `tinyweb_usr` should belong to the `webfiles` group and have no login shell (`/usr/sbin/nologin`). 

3. **Filesystem and Permissions**: Create a directory `/var/www/html` owned by `root` but with group `webfiles`. Set the permissions so that the group can read the contents, but others cannot. Place a file named `index.html` inside with the content `Welcome to the secure server`. 

4. **Web Server Setup & TLS**: Generate a self-signed TLS certificate and private key at `/etc/tinyweb/cert.pem` and `/etc/tinyweb/key.pem`. Configure the server to run as `tinyweb_usr`. The server should listen on port `8443` for HTTPS requests. 

5. **Idempotent Configuration**: Create a bash script at `/home/user/setup.sh` that performs all the user creation, directory creation, permission setting, and TLS certificate generation steps. This script must be fully idempotent (running it multiple times should not produce errors or unintended changes).

Finally, start the compiled web server in the background so it listens on `127.0.0.1:8443`.