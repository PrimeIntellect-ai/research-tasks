You are assisting a compliance officer who is auditing an internal network's access logs. 

Recently, the automated Bash script used to compute user access risk scores started producing wildly incorrect, inflated results. The officer suspects the previous developer wrote a script that accidentally creates an "implicit cross join" (a Cartesian product) when aggregating the log lines, artificially multiplying the number of connections.

Your task is to write a corrected Bash script at `/home/user/audit_paths.sh` that reliably computes the risk metrics.

First, you need to find the dynamic "Risk Threshold" ($T$). We received an attached surveillance snippet from the server room at `/app/audit_logs.mp4`. The system was configured to record exactly 1 frame for every failed login attempt in the last hour. 
Find the total number of frames in `/app/audit_logs.mp4`. This integer value is your Risk Threshold $T$.

Next, write your script at `/home/user/audit_paths.sh`.
The script must accept exactly one argument: the path to a text file containing the network access graph.
- The input file contains space-separated lines representing edges: `SourceNode DestinationNode`.
- Your script must compute the "out-degree" (the number of unique `DestinationNode`s) for each `SourceNode`.
- The script must filter and output only the `SourceNode`s whose out-degree is strictly greater than the Risk Threshold $T$.
- The output format must be exactly: `SourceNode OutDegree` (separated by a single space), one per line.
- The output must be sorted by OutDegree in descending order. If there is a tie, sort by `SourceNode` in ascending alphabetical order.
- You must use Bash and standard GNU coreutils/text processing tools (awk, sed, sort, uniq, etc.). Do not use Python, Perl, or other scripting languages.

Ensure your script handles standard edge cases (e.g., duplicated edges in the input should only be counted once per unique Source-Destination pair, avoiding the Cartesian product bug). The compliance automated test suite will aggressively test your script against hundreds of random log files to ensure strict equivalence with the expected behavior.