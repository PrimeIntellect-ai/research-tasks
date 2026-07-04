You are acting as a compliance officer auditing a legacy Identity and Access Management (IAM) system. The permission resolution engine recently crashed due to a "deadlock" caused by circular role inheritance. 

We need to audit the system's role inheritance graph to identify all privilege loops. Because the system is air-gapped and heavily restricted, you cannot install external graph databases (like Neo4j) or use languages other than standard Bash shell utilities (e.g., `awk`, `grep`, `join`, `sort`).

I have exported the current role inheritance graph to a tab-separated file located at `/home/user/iam_edges.tsv`. 
Each line contains two roles separated by a tab (`RoleA\tRoleB`), indicating that `RoleA` inherits all privileges from `RoleB` (a directed edge from RoleA to RoleB).

Your task is to:
1. Write a parameterized Bash script at `/home/user/find_cycles.sh` that takes exactly two arguments: the input edge file and the output file path.
   Usage: `./find_cycles.sh /home/user/iam_edges.tsv /home/user/deadlock_report.log`
2. The script must process the graph and materialize a projection of all circular dependencies (cycles) of **exactly length 3**. A length-3 cycle means RoleX inherits RoleY, RoleY inherits RoleZ, and RoleZ inherits RoleX (where X, Y, and Z are all distinct roles).
3. Format the output in the destination file as follows:
   - For each distinct cycle found, extract the three role names.
   - Sort the three role names alphabetically and join them with a hyphen (`-`). For example, if the cycle involves `dev`, `qa`, and `staging`, the string should be `dev-qa-staging`.
   - Ensure each cycle is listed only once.
   - Sort the final output file alphabetically.
4. Run your script to generate `/home/user/deadlock_report.log`.

Make sure the script is executable and relies entirely on Bash built-ins and standard coreutils/GNU utilities.