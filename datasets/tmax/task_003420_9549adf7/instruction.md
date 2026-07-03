You are a capacity planner tasked with building an automated, zero-downtime deployment pipeline for a resource usage analyzer. 

Your task involves writing a Rust-based analyzer and a bash deployment script (simulating a basic CI/CD pipeline) that handles directory linking, TLS setup, and web serving.

**Step 1: Write the Rust Analyzer**
Write a Rust program at `/home/user/src/analyzer.rs` that:
1. Reads a CSV file located at `/home/user/data/usage.csv`. The CSV has no header and contains rows in the format: `timestamp,cpu_percent,mem_mb` (e.g., `1670000000,45.5,1024`).
2. Calculates the arithmetic mean (average) of the `cpu_percent` and `mem_mb` columns.
3. Writes the output to a file named `report.json` in the *current working directory*. The JSON must exactly match this format:
`{"avg_cpu": <cpu_val>, "avg_mem": <mem_val>}`
*(Format numbers to 2 decimal places).*

**Step 2: Create the Deployment Pipeline**
Write a bash script at `/home/user/deploy.sh` that performs the following deployment sequence when executed:
1. Compiles `/home/user/src/analyzer.rs` into an executable named `analyzer` using `rustc`.
2. Creates a structured deployment directory: `/home/user/planner_app/releases/<timestamp>` (use standard unix epoch time for the timestamp).
3. Ensures a shared directory exists for TLS certificates at `/home/user/planner_app/shared/certs`.
4. Uses `openssl` to generate a self-signed RSA TLS certificate (`cert.pem`) and key (`key.pem`) in the `certs` directory *only if they do not already exist*. (Make them valid for 365 days, with a CN of `localhost`).
5. Copies the compiled `analyzer` binary into the newly created `<timestamp>` release directory.
6. Executes the `analyzer` binary *from within* the `<timestamp>` directory so that `report.json` is generated there.
7. Creates or updates a symlink at `/home/user/planner_app/current` to point to the newly created `<timestamp>` release directory.
8. Starts a secure static file server serving the `/home/user/planner_app/current` directory on TCP port `9443` in the background. You must use `openssl s_server` for this (e.g., `openssl s_server -quiet -key ... -cert ... -port 9443 -WWW -accept 9443`). Make sure to kill any previously running `openssl s_server` instances before starting the new one.

**Constraints:**
* Use standard standard coreutils and bash built-ins.
* Do not use external Rust crates (only `std`).
* The agent must be able to run `bash /home/user/deploy.sh` successfully to complete the task. Run it yourself as the final step to leave the server running.