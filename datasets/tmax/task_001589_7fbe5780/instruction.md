As a compliance officer, I am auditing our internal access delegation systems. We have a legacy, closed-source compliance engine located at `/app/legacy_auditor`. This stripped binary analyzes access grant logs to determine how a specific user obtained their privileges.

The binary reads a CSV from standard input with the format:
`grantor,grantee,timestamp,amount`
(where `timestamp` is a positive integer).
It takes exactly one argument: the `<target_user>`.
Example usage: `cat logs.csv | /app/legacy_auditor USER_Z`

It outputs a single line detailing the delegation path from the hardcoded root authority (`ADMIN`) to the `<target_user>`, along with a specific aggregated metric (which acts as a risk score). 

However, this binary is extremely slow on large datasets and we cannot inspect its logic directly. I need you to reverse-engineer its behavior (treating it as a black-box, or using tools like `strings`, `objdump`, or `strace` if you wish) and write a highly efficient, functionally identical replacement script in Bash. 

Your solution must be saved to `/home/user/new_auditor.sh`. It must accept the `<target_user>` as its first argument and read the CSV from standard input. 

Requirements:
1. You may use any standard Linux utilities available (e.g., `awk`, `sqlite3`, `sed`, `grep`, `sort`) within your Bash script to perform the necessary graph projection, path finding, and window/analytical aggregations.
2. The output of `/home/user/new_auditor.sh <target_user>` must match the output of `/app/legacy_auditor <target_user>` *byte-for-byte* for any valid CSV input.
3. Your script must be executable (`chmod +x`).

Take your time to generate sample inputs, feed them to `/app/legacy_auditor`, observe the outputs, and deduce the graph traversal rules (e.g., shortest path logic, tie-breaking mechanisms, and how the "risk score" / timestamp aggregation is calculated). Once you are confident, implement the exact equivalent in `/home/user/new_auditor.sh`.