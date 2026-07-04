You are an IT support technician responding to an escalated ticket (Ticket #8832). 

A data engineering team has provided a networking tool in `/home/user/ticket_8832/`. The tool is designed to read a pcap file, extract the TCP sequence numbers, and calculate the statistical variance of those sequence numbers. However, the team is reporting three issues:

1. **Build Failure:** The project won't build. Running `make` fails with an error. 
2. **Pcap Extraction Error:** Even when manually bypassing the build step, the bash script `process_pcap.sh` fails to extract the sequence numbers properly from the network capture.
3. **Numerical Instability:** When the team finally managed to pass numbers to the math script (`calc_variance.awk`), the calculated variance was `0.00` or wildly negative, which is mathematically impossible for their dataset. The sequence numbers in the capture are very large (around 1,000,000,000), but they do vary.

**Your Objectives:**
1. Diagnose and fix the build failure in the `Makefile`.
2. Fix `process_pcap.sh` so that it correctly extracts ONLY the absolute TCP sequence numbers from `traffic.pcap` (one number per line). You should use `tcpdump` for this.
3. Diagnose and fix the numerical instability in `calc_variance.awk`. The script currently uses the naive variance formula ($\frac{\sum x^2}{N} - (\frac{\sum x}{N})^2$). Because the TCP sequence numbers are extremely large, squaring them exceeds the 53-bit mantissa of standard double-precision floats used by `awk`, resulting in catastrophic cancellation. You must rewrite the `awk` script to use a numerically stable algorithm for calculating variance (e.g., Welford's online algorithm or a two-pass mean-deviation calculation).
4. Run the fixed build pipeline (which runs the process script and outputs the variance). 

Save the final, correctly calculated variance (formatted to exactly two decimal places, e.g., `123.45`) into a new file located at `/home/user/result.txt`.