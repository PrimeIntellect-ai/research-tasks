You are tasked with optimizing the network policy evaluation for a custom Kubernetes CNI (Container Network Interface) simulation. 

Our cluster uses a proprietary, top-down evaluated firewall and routing daemon. Currently, services are experiencing high latency and occasional timeouts due to a misconfiguration in how network policies are ordered. The daemon evaluates rules sequentially; each rule evaluated adds 1ms of latency to the connection establishment. 

You have been provided with:
1. `/app/policy_oracle`: A stripped, interactive binary that simulates the CNI policy engine.
2. `/home/user/base_policies.txt`: The current, unoptimized list of 200 Kubernetes network policy rules. Format: `RULE_ID SOURCE_CIDR DEST_CIDR ACTION` (where ACTION is ALLOW or DENY).
3. `/home/user/traffic_stats.csv`: A historical log of traffic frequencies. Format: `SOURCE_IP,DEST_IP,FREQUENCY_COUNT`.

Your objectives are:
1. **Analyze and Optimize (C Programming)**: Write a C program at `/home/user/optimizer.c` that compiles to `/home/user/optimizer`. This program must read `base_policies.txt` and `traffic_stats.csv`. It should reorder the rules to minimize the overall weighted connection latency (latency * frequency). Output the optimized rules to `/home/user/optimized_policies.txt` in the exact same format as the base policies.
   * *Hint:* To minimize latency, rules that resolve the most frequent traffic should be evaluated as early as possible. Be careful: reordering rules might change the effective action if a packet matches multiple conflicting rules (e.g., a specific ALLOW vs a broad DENY). Your reordered rules must maintain the *exact same* allow/deny outcomes as the base policies for every IP pair in the stats.

2. **Connectivity Diagnostics (Expect Scripting)**: The `/app/policy_oracle` binary takes the policy file as an argument (e.g., `/app/policy_oracle /home/user/optimized_policies.txt`) and drops into an interactive shell. In this shell, you can type `query <src_ip> <dst_ip>` and it will output `[ALLOW|DENY] <latency>ms`. 
   Write an Expect script at `/home/user/verify_connectivity.exp` that automates querying the oracle for the top 5 most frequent IP pairs to ensure they still result in `ALLOW` and to check their new latency.

3. **Idempotent Automation**: Write a bash script at `/home/user/apply.sh` that compiles your C program, runs it to generate the optimized file, and executes the Expect script. It should be idempotent (running it multiple times should yield the same correct state).

An automated verification suite will compile and run your C program, load your `optimized_policies.txt` into the oracle, and calculate the global average weighted latency across all traffic in the CSV. Your solution must preserve the original routing semantics while achieving the required performance metric.