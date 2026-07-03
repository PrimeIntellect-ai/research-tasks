You are acting as a capacity planner for our infrastructure team. We are setting up a secure log ingestion pipeline to analyze resource usage across our fleet, but we are facing issues with malformed and potentially malicious log injections from compromised nodes. 

Your objective is to build an automated, secure log validation and ingestion system.

**Part 1: Threshold Extraction**
An architectural diagram containing the critical capacity thresholds has been provided to you as an image at `/app/capacity_limits.png`. 
1. Extract the three integer values for `MAX_CPU`, `MAX_MEM`, and `MAX_DISK` from this image.
2. We have an interactive configuration tool located at `/home/user/bin/register_limits`. You must write an Expect script at `/home/user/setup_limits.exp` that automates running this tool and feeds it the three extracted integers when prompted. Run your script to register the limits.

**Part 2: Log Sanitiser Development (C)**
You must write a C program at `/home/user/sanitiser.c` and compile it to `/home/user/sanitiser`. This program will act as a security filter for incoming log files.
- **Invocation:** `./sanitiser <path_to_log_file>`
- **Format:** Each log file contains lines formatted as `timestamp,hostname,cpu,mem,disk`.
- **Validation:** 
  - Hostnames must only contain alphanumeric characters and hyphens (no shell metacharacters, spaces, or semicolons).
  - CPU, mem, and disk must be valid positive numbers.
- **Exit codes:** The program must return `0` if ALL lines in the file are valid, and `1` if ANY line is invalid or malicious.
- **Testing:** We have provided two directories of sample logs: `/app/corpus/clean/` containing valid metrics, and `/app/corpus/evil/` containing malicious or malformed logs (e.g., shell injection attempts, negative resources). Your sanitiser must successfully exit `0` for all files in the clean corpus, and `1` for all files in the evil corpus.

**Part 3: Secure Git Ingestion Pipeline**
We use Git to track and ingest log bundles from remote agents. 
1. Initialize a bare Git repository at `/home/user/metrics.git`.
2. Write a `pre-receive` Git hook in this repository. The hook must intercept incoming pushes, scan all pushed `.log` files using your compiled `/home/user/sanitiser`, and reject the push (exit non-zero) if the sanitiser flags any file.

**Part 4: Load Balancer Setup**
Finally, set up a local Nginx reverse proxy to act as the frontend for our capacity dashboards.
1. Create an Nginx configuration file at `/home/user/nginx.conf` that runs Nginx as an unprivileged user (listening on port `8080`).
2. Configure it to load balance HTTP requests in a round-robin fashion to two backend servers running on `127.0.0.1:8081` and `127.0.0.1:8082`.
3. Start the Nginx instance using this configuration.

Please ensure all scripts are executable and the Nginx service is running before completing the task.