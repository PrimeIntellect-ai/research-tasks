You are a Linux systems engineer tasked with hardening the configurations of several QEMU virtual machines. 

The startup scripts for these VMs are located in `/home/user/qemu_configs`. An initial audit has revealed two critical security issues:
1. Some scripts start the VMs with unsecured VNC access (e.g., containing the string `password=off` in the `-vnc` argument).
2. Some of these scripts have overly permissive filesystem permissions (specifically, they are world-writable).

Your task is to write a Python script at `/home/user/harden_vms.py` that automates the remediation of these issues. When run, your script must:
1. Scan the `/home/user/qemu_configs` directory for all `.sh` files.
2. Parse the contents of each file. If a file contains `password=off` as part of a `-vnc` argument, replace it with `password=on`. (Do not alter any other arguments or IP bindings).
3. Check the file permissions. If a file is world-writable (i.e., others have write access), change its permissions to `750` (rwxr-x---).
4. Generate a JSON report at `/home/user/hardening_report.json` that precisely matches this schema:
   ```json
   {
     "vnc_fixed": ["<filename1.sh>", "<filename2.sh>"],
     "permissions_fixed": ["<filename1.sh>", "<filename3.sh>"]
   }
   ```
   The lists should contain only the basenames of the files that were actually modified for each respective issue, sorted alphabetically.

Write the script and execute it so that the fixes are applied and the `hardening_report.json` file is generated. Ensure your code handles the file I/O safely and uses robust error handling.