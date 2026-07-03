You are a site administrator responsible for managing user accounts across our infrastructure. We have an automated user-sync pipeline that runs on a schedule to provision users across our containers and VMs, but it is currently broken.

Your task involves repairing the scheduled task runner, writing a high-performance user synchronization script in Go, and integrating the two.

**Step 1: Fix and Compile the Task Runner**
We use a custom, vendored version of `supercronic` (a cron compatible task runner) to run our jobs, located at `/app/supercronic`. 
Currently, it has a deliberate perturbation: a recent commit to `/app/supercronic/main.go` introduced a bug that overrides the `PATH` environment variable to a dummy value (`/tmp/wrongpath`), causing any scripts it runs to fail because standard system binaries cannot be found. 
Additionally, its `Makefile` has a typo in the build target name.
1. Find and fix the `PATH` bug in the vendored `supercronic` source.
2. Fix the `Makefile` so it correctly builds the binary.
3. Build the `supercronic` binary and place it at `/home/user/bin/supercronic`.

**Step 2: Write the Sync Script (`/home/user/sync_users.go`)**
Write a Go program that processes user account data. The program must:
1. **Connectivity Diagnostics**: Before processing, the script must verify that the target infrastructure is reachable. It should perform a TCP dial with a 1-second timeout to:
   - The QEMU VNC port: `localhost:5900`
   - The user metadata container port: `localhost:8080`
   If either connection fails, the script must exit with status code 1.
2. **Process Users**: Read a CSV file located at `/home/user/data/users.csv` (which will contain around 200,000 rows). The CSV has two columns: `username,role`.
3. **Transform**: For each user, compute a SHA-256 hash of the string `username+role`.
4. **Output**: Write a JSON file to `/home/user/sync_out.json` containing an array of objects, where each object has `"username"`, `"role"`, and `"hash"`.
5. **Performance**: Processing 200,000 records sequentially will be too slow for our metric threshold. You **must** use Go routines (concurrency) to process the hashes and build the output. The execution time of your compiled Go binary must be under **1.5 seconds**.

**Step 3: Configuration**
Create a crontab file at `/home/user/sync.cron` that schedules your compiled `sync_users` binary to run every minute (`* * * * *`). 

Compile your Go script to `/home/user/bin/sync_users`. Verify that running `/home/user/bin/supercronic /home/user/sync.cron` successfully executes your script, finds the system binaries (if you used any), connects to the ports, and writes the JSON file rapidly.