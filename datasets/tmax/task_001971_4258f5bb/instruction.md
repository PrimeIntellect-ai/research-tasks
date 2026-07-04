You are acting as a network security engineer investigating a series of suspected data exfiltration events. We have intercepted a large packet capture file located at `/home/user/traffic.pcap`. 

We have an internal tool called `fast-pcap-extract` used for analyzing PCAP files, extracting suspicious TCP payloads, calculating their SHA-256 hashes, and storing them for analysis. However, the latest version of the source code is currently broken and extremely slow.

Your task is to fix, secure, and optimize this tool, then use it to extract the suspicious payloads.

**Task Steps:**

1. **Fix the Vendored Package:**
   The source code is located at `/app/fast-pcap-extract-1.2`. 
   - The `Makefile` is currently broken (it fails to link the final executable correctly). Fix the Makefile so that typing `make` successfully builds the `./pcap_extract` binary.

2. **Vulnerability Remediation & Access Control:**
   - There are two critical security flaws in `parser.c` and `writer.c`. Use a vulnerability scanner or manual code review to find them. 
   - Fix the buffer overflow vulnerability when parsing the packet headers.
   - Fix the insecure file creation bug. The tool currently creates the extracted payload files and the `hashes.txt` file with world-readable permissions. You must modify the C code so that these files are created with strict `600` (`rw-------`) permissions, and the output directory itself is created with `700` permissions.

3. **Performance Optimization:**
   - The payload matching logic in `matcher.c` uses a naive, highly unoptimized nested loop to search for the malicious signature byte sequence. 
   - Optimize this routine (e.g., using `memmem`, KMP, or other efficient searching algorithms) and ensure appropriate compiler optimization flags are used. 
   - To pass the automated verification, your optimized binary must process a massive evaluation PCAP and achieve a **runtime speedup of at least 3.0x** compared to the naive implementation.

4. **Execution:**
   - Run your compiled, secured, and optimized `./pcap_extract` binary on the provided capture file:
     `./pcap_extract /home/user/traffic.pcap /home/user/extracted_payloads`
   - The tool will automatically output the payloads and a `hashes.txt` file containing the SHA-256 checksums of the payloads to the target directory.

Ensure the final state of `/home/user/extracted_payloads/hashes.txt` contains the correct SHA-256 hashes of the extracted payloads, and that all permissions strictly adhere to the requirements.