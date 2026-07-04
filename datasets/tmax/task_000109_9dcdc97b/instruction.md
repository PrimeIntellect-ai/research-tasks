You are acting as an infrastructure engineer automating the provisioning of tenant directories on our storage server. 

We need a short, interactive Python script located at `/home/user/provision.py` that handles local filesystem provisioning and basic storage checks for new users. 

Write the Python script (`/home/user/provision.py`) to meet the following exact requirements:
1. When executed, the script must prompt the user via standard input exactly with: `Enter username: `
2. It must read the username from standard input.
3. It must check the available free disk space on the partition hosting `/home/user/tenants`. If the free space is less than 100 Megabytes (100 * 1024 * 1024 bytes), it should print `Error: Insufficient disk space` to standard output and exit with status code 1.
4. If space is sufficient, it must create a directory structure for the tenant:
   - `/home/user/tenants/<username>/data`
   - `/home/user/tenants/<username>/logs`
   (Assume `/home/user/tenants` already exists, but the user's directory might not).
5. It must create a file named `.quota` inside `/home/user/tenants/<username>/` containing exactly the string `10GB` (no trailing newline is required, but it's acceptable).
6. It must append a log entry to `/home/user/provision_log.txt` in the exact format: `Provisioned <username>\n` (e.g., `Provisioned alice`).
7. Finally, it should print `Success` to standard output and exit with status code 0.

Ensure your script is executable or can be run directly via `python3 /home/user/provision.py`. Do not create the `/home/user/tenants` directory yourself in the task response; just write the script.