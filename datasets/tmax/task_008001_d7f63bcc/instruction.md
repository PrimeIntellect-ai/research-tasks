You are acting as a FinOps engineer optimizing our local edge-cache deployments. To delay costly volume expansions, we dynamically route incoming cache writes to the local caching instance that currently consumes the least disk space.

You need to create a solution that monitors disk usage, processes the results, and idempotently generates a reverse proxy configuration snippet using a custom C program.

Here is the environment and requirements:
1. We have three cache directories: `/home/user/cache_a`, `/home/user/cache_b`, and `/home/user/cache_c`.
2. Each cache directory corresponds to a local cache service listening on a specific port:
   - `cache_a` -> Port `8081`
   - `cache_b` -> Port `8082`
   - `cache_c` -> Port `8083`

Step 1: Write a C program at `/home/user/deploy_proxy.c` and compile it to `/home/user/deploy_proxy`.
- The program must take exactly one command-line argument: the name of the selected cache directory (e.g., `cache_a`, `cache_b`, or `cache_c`).
- It should map the provided directory name to its corresponding port.
- It must idempotently write the following exact configuration string to `/home/user/proxy_backend.conf`:
  `backend best_cache { server 127.0.0.1:<PORT>; }`
  (Replace `<PORT>` with the correct port number. Ensure there is a newline at the end of the file. If the file exists, it must be completely overwritten).

Step 2: Write a bash script at `/home/user/optimize_storage.sh` (ensure it is executable).
- The script must use standard text processing tools (like `du`, `sort`, `awk`, `head`, etc.) to calculate the total disk usage of `/home/user/cache_a`, `/home/user/cache_b`, and `/home/user/cache_c`.
- It must identify the directory with the *smallest* current disk usage (in bytes or KB).
- It must extract just the base name of that directory (e.g., `cache_b`).
- Finally, it must execute `/home/user/deploy_proxy <DIRECTORY_NAME>` to generate the load balancer configuration.

Step 3: Run `/home/user/optimize_storage.sh` so that `/home/user/proxy_backend.conf` is correctly generated based on the current storage state.