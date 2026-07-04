You are a FinOps analyst working to reduce cloud storage and data transfer costs. Your team generates monthly cost reports, which are currently duplicated across multiple environments. To test a new local caching strategy before deploying it to the cloud, you need to structure the existing reports using symlinks, generate a TLS certificate interactively (simulating a legacy strict-prompt internal tool), and set up a secure local web server.

Perform the following tasks:

1. **Directory and Link Management**: 
   You will find raw report files in `/home/user/raw_reports/`. They are named in the format `cost_report_YYYY_MM.html`. 
   Create a new directory structure under `/home/user/finops_web/`. For every report in the raw directory, create a symbolic link at `/home/user/finops_web/YYYY/MM/index.html` pointing to the corresponding raw report file.

2. **Interactive Automation for TLS**:
   Due to legacy compliance tools, you are not allowed to use the `-subj` flag or batch mode in OpenSSL to create your certificate. You must write an `expect` script located at `/home/user/gen_cert.exp`.
   This script must execute exactly this command:
   `openssl req -x509 -newkey rsa:2048 -nodes -keyout /home/user/key.pem -out /home/user/cert.pem -days 365`
   
   The `expect` script must interactively answer the prompts with the following exact values:
   - Country Name: `US`
   - State or Province Name: `California`
   - Locality Name: `San Francisco`
   - Organization Name: `CloudCo`
   - Organizational Unit Name: `FinOps`
   - Common Name: `localhost`
   - Email Address: `admin@cloudco.local`

   Run your `expect` script to generate `/home/user/cert.pem` and `/home/user/key.pem`.

3. **Web Server Setup**:
   Create an executable Bash script at `/home/user/start_server.sh`. When executed, this script should start a background process (using Python or any standard tool available) that serves the `/home/user/finops_web/` directory over HTTPS on port `8443`, using the `cert.pem` and `key.pem` files you generated. The script must write the Process ID (PID) of this background web server to `/home/user/server.pid`.

Run your `start_server.sh` script so the server is actively listening.