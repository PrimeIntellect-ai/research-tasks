You are a DevOps engineer tasked with debugging a regression in a network analysis tool. 

The repository located at `/home/user/net-parser` contains a Bash script named `parse_trace.sh`. This script is designed to process intermediate network packet trace files (textual representations of pcap analyses) and extract all unique IPv4 addresses associated with connection events. 

Recently, the monitoring pipeline started exhibiting intermittent failures. Some critical IP addresses are being missed during the format parsing phase, specifically when intermediate state traces include unexpected whitespace or varied prefixes (e.g., "Src IP:" vs "Source:"). 

You know the following:
1. The repository has roughly 200 commits. 
2. The script worked perfectly at tag `v1.0` (which is the very first commit).
3. The current `HEAD` of the `main` branch is failing on the provided edge-case trace file located at `/home/user/edge_case_trace.log`.

Your objectives are:
1. **Bisect the regression**: Find the exact commit hash that introduced the bug. Write this full commit hash to `/home/user/bad_commit.txt`.
2. **Fix the bug**: Identify the parsing edge-case that was mishandled. Fix `parse_trace.sh` at the `HEAD` of the `main` branch so it correctly extracts all valid IPv4 addresses from `/home/user/edge_case_trace.log`, regardless of the preceding text or spacing on the line. The output should be a newline-separated list of unique IPv4 addresses, sorted alphabetically.
3. Save your corrected version of the script to `/home/user/parse_trace_fixed.sh` and ensure it is executable.

To complete this task, you will need to utilize `git bisect`, carefully analyze intermediate states, and repair the format parsing logic in Bash.