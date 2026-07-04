You are a forensics engineer investigating a severe issue in a long-running C-based network service. 
The service, `packet_processor`, has been experiencing spontaneous out-of-memory (OOM) crashes in production. We suspect a specific malicious network packet is triggering an infinite loop combined with a memory leak.

You have been provided with an Apptainer-compatible workspace at `/home/user/app/`. In this directory, you will find:
1. `packet_processor.c`: The source code of the vulnerable service. It uses `libpcap` to read network packets.
2. `traffic.pcap`: A packet capture file containing normal traffic and a single "poison" packet that triggers the vulnerability.
3. `Makefile`: To compile the program.

Your objectives:
1. **Analyze the PCAP and Code:** Inspect `packet_processor.c` and use packet analysis tools (like `tcpdump` or `tshark`) on `traffic.pcap` to identify the bug. Look for how a specific payload structure could cause loop termination failure and a subsequent memory leak.
2. **Identify the Attacker:** Determine the source IP address of the malicious UDP packet that triggers the infinite loop. Write this IP address into a file named `/home/user/attacker_ip.txt`.
3. **Fix the Vulnerability:** Modify `packet_processor.c` to fix the loop termination bug (ensure the parser offset advances correctly) AND fix the memory leak (ensure allocated memory is freed or not leaked during parsing).
4. **Compile the Fix:** Run `make` to compile your fixed program. The resulting binary must be named `packet_processor`.

**Verification:**
An automated test suite will run your fixed `packet_processor` against the `traffic.pcap` file. 
To pass, your program must process the entire pcap file and exit cleanly with a code of `0` in under 2 seconds (proving the infinite loop is fixed and memory does not exhaust). The `/home/user/attacker_ip.txt` must contain exactly the attacker's IPv4 address.