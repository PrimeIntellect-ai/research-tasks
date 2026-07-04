You are managing a legacy user provisioning system as a site administrator. We have an old interactive C program that generates standard user profile files, but we need to automate its usage for batch processing and securely serve the generated profiles over an HTTPS server managed by a process supervisor. 

Please perform the following tasks in the `/home/user` directory:

1. **Compile the Legacy Provisioner:**
   You will find a file named `/home/user/user_prov.c`. Compile it to an executable named `/home/user/user_prov` using `gcc`.

2. **Automate with Expect:**
   The `user_prov` program interactively prompts for "Enter username: " and then "Enter department: ". 
   Write an Expect script at `/home/user/auto_prov.exp` that accepts exactly two command-line arguments (username and department), spawns `/home/user/user_prov`, and interacts with it by providing the arguments to the prompts.

3. **Batch Processing Script:**
   There is a file `/home/user/users.csv` containing a list of users in the format `username,department`.
   Write a bash script at `/home/user/batch_prov.sh` that reads this CSV file and uses your `auto_prov.exp` script to generate profiles for all users. The C program will create files named `<username>_profile.txt` in the current directory. 
   Your script must ensure the `public_html` directory exists (`/home/user/public_html/`) and move all generated `*_profile.txt` files into it. Execute your script to generate the profiles.

4. **TLS & Web Server Configuration:**
   Create a directory `/home/user/certs/` and generate a self-signed RSA 2048-bit certificate (`cert.pem`) and unencrypted private key (`key.pem`) valid for 365 days. 
   Write a Python script at `/home/user/https_server.py` that acts as a simple web server serving the contents of `/home/user/public_html/` over HTTPS on port 8443 using the TLS certificates you generated. 

5. **Process Supervision:**
   We need the web server to run reliably in the background. Create a Supervisor configuration file at `/home/user/supervisord.conf` that manages the `https_server.py` script. 
   The supervisor configuration should have a `[program:webserver]` section. Set its command to run your python script. Configure it to write standard out and standard error logs to `/home/user/logs/webserver.log` (ensure the `/home/user/logs/` directory exists).
   Finally, start `supervisord` using your configuration file so that the web server is running in the background.

Verify your setup is working: an automated test will use `curl -k https://127.0.0.1:8443/alice_profile.txt` to ensure the profiles are correctly served.