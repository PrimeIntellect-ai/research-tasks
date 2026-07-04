You are a support engineer investigating a regression in our network diagnostics pipeline. Our pipeline uses a bash script to extract summary data from packet capture (pcap) files, but a recent change caused it to output incorrect data, leading to downstream errors.

You have been provided with the following files in `/home/user/`:
- `traffic.pcap`: A sample packet capture file containing a mix of TCP and UDP traffic.
- `transform.sh`: The buggy bash script that reads a pcap file (using `tcpdump`) and outputs a CSV with columns: `Source_IP,Dest_IP,Protocol,Length`.
- `expected.csv`: The correct CSV output that `transform.sh` should produce when run against `traffic.pcap`.

Your tasks are:
1. Analyze the packet capture and the output of the current `transform.sh` to identify the bug. The bug is related to how the IP addresses and protocols are extracted from the `tcpdump` output.
2. Fix `/home/user/transform.sh` using only Bash built-ins, coreutils (like `awk`, `sed`, `grep`), and `tcpdump`. Ensure it correctly handles both TCP and UDP packets and extracts the base IP address (stripping off the port).
3. Create a regression test script at `/home/user/test.sh`. This script must:
   - Run `./transform.sh traffic.pcap` and save the output to a temporary file.
   - Run a diff between the generated output and `expected.csv`.
   - Save the exact output of the `diff -u expected.csv <generated_output>` command to `/home/user/diff.log`.
   - Exit with code 0 if the diff is empty (meaning the output is perfectly correct), or exit with code 1 if there are differences.
   - Make sure `test.sh` is executable.

Constraints:
- You must write the logic in Bash and standard GNU tools.
- The output CSV must include a header: `Source_IP,Dest_IP,Protocol,Length`
- IP addresses in the output must not include the port numbers (e.g., `10.0.0.1`, not `10.0.0.1.80`).
- Do not modify `traffic.pcap` or `expected.csv`.

When you have fixed the script, run `./test.sh` to verify your solution.