You are a Linux systems engineer tasked with hardening a server configuration. You need to create a filesystem integrity monitor in Rust, schedule its execution, and prepare a network routing and interface hardening script. 

Follow these exact steps:

1. **Network Configuration Script**
   Create an executable bash script at `/home/user/harden_net.sh`. Because you do not have root privileges, you will not run this script, but it must be prepared for a privileged user.
   The script must contain the exact `ip` commands to:
   - Add a blackhole route for the suspicious subnet `203.0.113.0/24`.
   - Set the MTU of the `eth0` interface to `1400`.

2. **Filesystem Setup**
   Create the directory `/home/user/secure_configs/`.
   Inside this directory, create two configuration files exactly as follows (do NOT include trailing newlines in these files):
   - `/home/user/secure_configs/app.conf` containing exactly the text: `PORT=8080`
   - `/home/user/secure_configs/db.conf` containing exactly the text: `MAX_CONNS=50`

3. **Rust Integrity Monitor**
   Create a new Rust binary project at `/home/user/fs_monitor`. 
   Write a Rust program that reads all files in `/home/user/secure_configs/`, computes their SHA-256 hashes, and writes a JSON report to `/home/user/audit_report.json`.
   
   The output JSON format must exactly match this structure (with the actual hex hashes):
   ```json
   {
     "files": [
       {
         "name": "app.conf",
         "hash": "<sha256_hex_string_here>"
       },
       {
         "name": "db.conf",
         "hash": "<sha256_hex_string_here>"
       }
     ]
   }
   ```
   **Important constraints for the Rust program:**
   - The array of files in the JSON output must be sorted alphabetically by the file `name`.
   - Build the program using `cargo build --release`.
   - Execute the compiled binary once manually so that `/home/user/audit_report.json` is generated.

4. **Scheduled Task Configuration**
   Configure a user cron job to execute the compiled Rust binary automatically. 
   Add an entry to your crontab that runs `/home/user/fs_monitor/target/release/fs_monitor` exactly every 15 minutes. 
   The cron job must redirect standard error (`stderr`) to `/home/user/fs_monitor_error.log`. Do not redirect standard output (`stdout`).

Ensure all files, directories, and cron jobs exist exactly as specified.