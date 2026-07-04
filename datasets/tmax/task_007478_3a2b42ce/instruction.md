You are a Linux systems engineer tasked with building a custom hardening auditing tool. Since we are testing this in a non-root environment, you will operate on mock system configuration files located in `/home/user/`.

Your task is to write a C++ program, `auditor.cpp`, and a bash execution script, `audit_job.sh`, that evaluates three primitive systems areas: user groups, network routing, and disk quotas.

**Phase 1: Understand the Inputs**
You will parse three files provided in `/home/user/`:
1. `/home/user/mock_group`: Formatted exactly like `/etc/group` (e.g., `group_name:password:GID:user_list`).
2. `/home/user/mock_route`: Formatted exactly like `/proc/net/route` (columns separated by tabs).
3. `/home/user/mock_quota`: A plain text file with lines formatted as: `username:used_bytes:quota_bytes`.

**Phase 2: The C++ Auditor Tool**
Write `/home/user/auditor.cpp`. It must take exactly three command-line arguments in this order: path to the group file, path to the route file, and path to the quota file.

It must perform the following hardening checks and output the results to standard output:
1. **Group Check**: Read the group file. The `admin` group must ONLY contain the users `alice` and/or `bob`. If any other user is in the `admin` group, the check fails.
2. **Route Check**: Read the route file. A default route (Destination `00000000`) MUST exist on `eth0`. Additionally, NO routes should exist for the `wlan0` interface. If either condition is violated, the check fails.
3. **Quota Check**: Read the quota file. If any user's `used_bytes` is strictly greater than 80% of their `quota_bytes`, the check fails.

**Phase 3: Output Format**
The C++ program must print exactly three lines to standard output:
Line 1: `GROUP_CHECK: PASS` OR `GROUP_CHECK: FAIL (<comma-separated list of unauthorized users in admin>)`
Line 2: `ROUTE_CHECK: PASS` OR `ROUTE_CHECK: FAIL`
Line 3: `QUOTA_CHECK: PASS` OR `QUOTA_CHECK: FAIL (<comma-separated list of users exceeding 80% quota>)`
*Note: comma-separated lists must be alphabetically sorted and contain no spaces.*

**Phase 4: Execution Script**
Write a bash script at `/home/user/audit_job.sh` that:
1. Compiles `/home/user/auditor.cpp` using `g++ -std=c++17 -o /home/user/auditor /home/user/auditor.cpp`.
2. Executes the compiled binary with the paths to the mock files: `/home/user/mock_group`, `/home/user/mock_route`, `/home/user/mock_quota`.
3. Redirects the output to `/home/user/report.log`.

Execute your bash script to generate the final `/home/user/report.log`.