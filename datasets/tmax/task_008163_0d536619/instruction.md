You are acting as a FinOps analyst working to optimize cloud costs. Our team has identified that an expensive 3rd-party API used for calculating real-time usage costs can be replaced by a lightweight, locally hosted microservice on our edge nodes. 

Your task is to build and configure this local stack in `/home/user/`. Because you are working in a restrictive edge environment without root access, you must configure user-space networking and process management.

Step 1: The Rust Cost Calculator
Create a Rust project named `cost-analyzer` in `/home/user/cost-analyzer`. 
Write a simple multi-threaded TCP server in `src/main.rs` (using only the standard library, no external crates in Cargo.toml) that does the following:
- Accepts a port number as a command-line argument (e.g., `cargo run -- 8081`).
- Listens on `127.0.0.1:<port>`.
- Whenever a client connects and sends a number (representing usage hours, e.g., `100\n`), the server should multiply it by `0.15` (our internal instance rate) and return the result formatted to exactly two decimal places, followed by a newline (e.g., `15.00\n`), and then close the connection.

Step 2: Reverse Proxy & Load Balancing
We will run three instances of your Rust service for high availability.
Create an HAProxy configuration file at `/home/user/haproxy.cfg`.
Configure it to listen on `127.0.0.1:8080` (mode tcp) and balance connections (using roundrobin) across three backend servers running on `127.0.0.1:8081`, `127.0.0.1:8082`, and `127.0.0.1:8083`. 

Step 3: Process Supervision
Write a bash script at `/home/user/supervisor.sh`. 
When executed, this script should:
- Start the HAProxy instance in the background using your config file.
- Start three instances of the compiled Rust `cost-analyzer` binary on ports 8081, 8082, and 8083 in the background.
- Implement a basic monitoring loop: every 5 seconds, check if the Rust processes are still running. If any of the three backend processes crash or are killed, the script must automatically restart the missing instance on its assigned port.

Step 4: Ephemeral Storage (fstab config)
To save on EBS volume I/O costs, we want to store temporary calculation logs in RAM. Since you don't have root access to run the `mount` command, the infrastructure team will do it for you. 
Write exactly one line into `/home/user/fstab_entry.txt` representing the `/etc/fstab` entry required to mount a `tmpfs` volume at `/home/user/reports`. It must have a size limit of `50M` and be restricted to user ID 1000 and group ID 1000.

Step 5: Backup Strategy
Write a bash script at `/home/user/backup.sh`. When executed, it must create a compressed tar archive of the `/home/user/reports/` directory and save it to `/home/user/backups/reports_backup.tar.gz`. Ensure the script creates the `/home/user/backups/` directory if it does not already exist.

Verify your setup by compiling the Rust binary, ensuring the scripts have executable permissions, and outputting your files in the exact paths requested.