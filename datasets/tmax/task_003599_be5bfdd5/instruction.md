You are a FinOps analyst tasked with optimizing cloud network egress costs. Our system routes traffic through multiple interfaces, each with different per-GB data transfer costs. However, our current routing configuration is sub-optimal.

You need to analyze the network flows, write a C program to determine the most cost-effective valid routing assignments, and generate an idempotent shell script to apply the changes.

Your final deliverables will be evaluated based on the exact contents of specific output files.

### Inputs Provided
You will find the following files in `/home/user/`:
1. `raw_flows.log` - Contains recent network traffic logs. 
   Format: `[TIMESTAMP] [SRC_IP] [DST_IP] [BYTES_TRANSFERRED] [CURRENT_INTERFACE]`
2. `pricing.csv` - Contains the cost per Gigabyte (GB, where 1 GB = 1073741824 bytes) for each network interface.
   Format: `INTERFACE_NAME,COST_PER_GB_IN_USD`
3. `allowed_routes.txt` - Defines which interfaces are permitted to route traffic to specific destination IPs.
   Format: `DST_IP ALLOWED_IFACE_1 ALLOWED_IFACE_2 ...`

*(Note: These files have been pre-populated in your environment).*

### Phase 1: Text Processing Pipeline
Write a bash script named `/home/user/aggregate_flows.sh` that processes `raw_flows.log`.
- It must aggregate the total bytes transferred to each `DST_IP` using the *current* interface.
- It must output the results to `/home/user/aggregated_flows.txt` in the format: `DST_IP CURRENT_INTERFACE TOTAL_BYTES`
- Ensure your script handles multiple log entries for the same destination and interface by summing their bytes.

### Phase 2: Cost Optimization in C
Write a C program at `/home/user/cost_optimizer.c`. Your program must:
1. Read `/home/user/aggregated_flows.txt`, `/home/user/pricing.csv`, and `/home/user/allowed_routes.txt`.
2. For each `DST_IP` in the aggregated flows:
   - Calculate the *current* cost based on the current interface's price and total bytes (convert bytes to GB as a floating point number).
   - Determine the *cheapest allowed* interface for that `DST_IP` from `allowed_routes.txt`.
   - Calculate the *optimized* cost if the traffic were routed through this cheapest interface.
   - Calculate the savings (Current Cost - Optimized Cost).
3. Output the overall system savings to a file named `/home/user/savings.log` in exactly this format:
   `Total Savings: $<amount>` (rounded to 2 decimal places, e.g., `Total Savings: $45.23`).
4. Generate a bash script at `/home/user/update_routes.sh` that updates the routing table to the optimized interfaces.
   - For every `DST_IP` analyzed, the script should output an idempotent `ip route replace` command:
     `ip route replace <DST_IP> dev <OPTIMIZED_INTERFACE>`
   - The script must start with `#!/bin/bash`.
   - Set the script's execution permissions (e.g., `chmod +x`).

### Phase 3: Automation
Write a master script `/home/user/run_optimization.sh` that:
1. Compiles your C program using `gcc` into `/home/user/cost_optimizer`.
2. Executes `/home/user/aggregate_flows.sh`.
3. Executes `/home/user/cost_optimizer`.

**Constraints & Notes:**
- Do NOT use root or sudo commands. The `update_routes.sh` script is meant to be verified programmatically and does not need to be executed by you.
- Write standard C99/C11 code. You may use standard libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.).
- Ensure that you accurately calculate GB using `1073741824` bytes.
- Run `/home/user/run_optimization.sh` once you are done so the output files are generated for automated verification.