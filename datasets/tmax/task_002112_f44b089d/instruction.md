You are an infrastructure engineer tasked with automating the provisioning of a legacy application. You must write a highly efficient, concurrent Python script to deploy multiple instances of this application, while also preparing the necessary user accounts, firewall rules, and log rotation configurations.

The specifications for this deployment are provided in an image file located at `/app/provision_specs.png`. You will need to extract three key values from this image:
1. `Username`
2. `StartPort`
3. `RotateSize`

You must write a master provisioning script in Python at `/home/user/provision.py`. When run, your script must perform the following tasks:

1. **Extract Specs:** Programmatically read the values from `/app/provision_specs.png` (using OCR tools like `pytesseract` which are available).
2. **User Account Administration:** Generate a bash script at `/home/user/create_users.sh`. This script should contain commands to create 10 users sequentially, named `<Username>_0` through `<Username>_9`. Use the format: `useradd -m -s /bin/bash <Username>_<ID>`.
3. **Log Configuration:** Generate a `logrotate` configuration file at `/home/user/service_logrotate.conf`. It must target `/home/user/logs/service_*.log`, rotate daily, use the `size` directive with the `<RotateSize>` extracted from the image, and keep 7 backups. Include `missingok` and `compress`.
4. **Firewall Rules:** Generate a bash script at `/home/user/firewall.sh` containing `iptables` commands to forward incoming external ports `8000` through `8009` to the respective internal service ports (`<StartPort>` through `<StartPort>+9`). Use the format: `iptables -t nat -A PREROUTING -p tcp --dport <ExternalPort> -j REDIRECT --to-port <InternalPort>`.
5. **Interactive Provisioning (Expect Scripting):** There is an interactive legacy installer located at `/app/legacy_installer.py`. You must run this installer 10 times (for instance IDs 0 through 9). 
   - Execute the installer as: `python3 /app/legacy_installer.py <ID>`
   - The installer will prompt: `"Enter Admin Username: "` -> provide `<Username>_<ID>`
   - The installer will prompt: `"Enter Service Port: "` -> provide `<StartPort> + ID`
   - You must use Python's `pexpect` or standard `subprocess` with pipe handling to automate this interaction.
6. **Concurrency & Performance:** The legacy installer is heavily rate-limited and contains artificial delays (taking exactly 2 seconds per execution). If you run the 10 instances sequentially, your script will take over 20 seconds. **You must parallelize the execution of the 10 installers** using `asyncio`, `threading`, or multiprocessing. Your script `/home/user/provision.py` must complete the entire setup in under 4 seconds.

Constraints:
- Ensure `/home/user/logs/` directory is created by your Python script before the installers run.
- Your script `/home/user/provision.py` must be executable (`chmod +x`).
- Do NOT run the bash scripts you generate (`create_users.sh`, `firewall.sh`), just generate them accurately.

The automated verification will run `/home/user/provision.py` and strictly measure its execution time, evaluating the speedup against a sequential reference implementation, and will verify the contents of the generated configuration files.