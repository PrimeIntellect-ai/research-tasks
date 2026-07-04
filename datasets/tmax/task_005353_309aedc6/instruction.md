You are a system administrator tasked with deploying a secure, interactive C-based web application backend. 

You need to compile the setup application, automate its interactive user configuration using `expect`, prepare the required directory structure with symlinks, and start a local TLS-secured file server.

Follow these steps exactly:

1. **Compilation**: 
   A C source file exists at `/home/user/src/setup.c`. Compile it into an executable located at `/home/user/bin/setup` (create the `bin` directory if it does not exist).

2. **Directory and Link Management**:
   Create the following directories:
   - `/home/user/deploy/webroot`
   - `/home/user/deploy/certs`
   - `/home/user/shared_assets`
   
   Create a symbolic link at `/home/user/deploy/webroot/assets` that points to `/home/user/shared_assets`.
   Create a test file `/home/user/shared_assets/test.txt` containing the text: `Assets working`.

3. **Expect Scripting (User Admin Simulation)**:
   The `setup` binary you compiled is an interactive tool for initializing the application's user database. It takes one argument: the output path for the database.
   Write an `expect` script at `/home/user/bin/run_setup.exp` that automates running:
   `/home/user/bin/setup /home/user/deploy/users.db`
   
   The interactive prompts and expected inputs are:
   - Prompt: `Enter admin pin: ` -> Input: `9922`
   - Prompt: `Enter new username: ` -> Input: `app_admin`
   - Prompt: `Enter new password: ` -> Input: `SecureDeploy2024`
   
   Run your `expect` script to successfully generate `/home/user/deploy/users.db`.

4. **TLS Configuration and Web Server Setup**:
   Generate a self-signed RSA 2048-bit TLS certificate and private key in `/home/user/deploy/certs/` named `cert.pem` and `key.pem` respectively. (Use `-nodes` and any subject `/CN=localhost`).
   
   Using OpenSSL's built-in web server capability, start a background process serving files from `/home/user/deploy/webroot` over HTTPS on port `8443`.
   Command hint: `openssl s_server -WWW -cert <path-to-cert> -key <path-to-key> -accept 8443`
   Ensure this process runs in the background and its stdout/stderr are redirected to `/home/user/deploy/server.log`.

Make sure the server is left running in the background when your terminal session ends.