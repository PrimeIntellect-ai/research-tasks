You are tasked with debugging a regression in a Python tool that analyzes trading data from network packet captures. 

Recently, our downstream accounting system started complaining about precision loss in the trade prices extracted from the network traffic. We have a Git repository located at `/home/user/repo` which contains the tool `parse_pcap.py`. We know that 200 commits ago (the root commit), the script worked perfectly and extracted full-precision prices (e.g., 14 decimals). Sometime between then and the current `HEAD`, a developer modified the parsing logic to handle a format parsing edge case (malformed trailing characters), but accidentally introduced a precision loss bug.

Your tasks are:
1. Analyze the packet capture `/home/user/test_traffic.pcap` to understand the expected payload format.
2. Use `git bisect` in `/home/user/repo` to find the exact commit that introduced the precision loss regression. The script `test_runner.py` in the repo can be used to check if the current commit is good or bad (it returns exit code 0 if good, 1 if bad).
3. Once you find the bad commit hash, save it to `/home/user/bad_commit.txt`.
4. At the current `HEAD` of the repository, fix the bug in `parse_pcap.py` so that it extracts the full precision float without failing on the edge cases (like trailing non-numeric garbage).
5. Create a minimal reproducible example script at `/home/user/mre.py` that isolates the buggy function from the bad commit, passes in a hardcoded byte string representing a packet payload (e.g., `b"TRADE MSG PRICE=123.456789012345XYZ"`), and prints the parsed float. This script should NOT require reading the pcap file.

Ensure your fix in `parse_pcap.py` correctly parses all packets in the pcap file with full precision.