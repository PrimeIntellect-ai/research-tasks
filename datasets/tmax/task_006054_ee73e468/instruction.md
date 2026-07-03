You are tasked with debugging and fixing a regression in a Rust packet analysis tool. 

The repository is located at `/home/user/flow-analyzer`. This tool reads a `.pcap` file and calculates a moving average of packet sizes over specific sequence windows. 

Recently, a regression was introduced. The tool works perfectly on the `v1.0` tag, but the current `main` branch panics due to an index out of bounds or numerical error when processing the capture file located at `/home/user/trace.pcap`.

Your tasks:
1. Use `git bisect` (or any other method) to find the exact commit that introduced the regression between the `v1.0` tag and `main`.
2. Write the full 40-character git commit hash of the bad commit to `/home/user/bad_commit.txt`.
3. Diagnose and fix the boundary condition / off-by-one bug in the current `main` branch (do not just checkout the old commit; fix the bug in the latest `main` code).
4. Recompile the tool and run it against `/home/user/trace.pcap`.
5. Save the standard output of the fixed tool to `/home/user/output.txt`.

Ensure your fix correctly handles the boundary logic without masking other potential data inconsistencies.