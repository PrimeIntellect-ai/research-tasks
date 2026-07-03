You are a security researcher analyzing a suspicious application bundle found on a compromised server. You have been provided with three disorganized log files and a C source file for a binary that the attackers were running. 

Your investigation has several phases:

1. **Log Timeline Reconstruction:**
   The attackers split their access logs into three separate files located at:
   - `/home/user/service_alpha.log`
   - `/home/user/service_beta.log`
   - `/home/user/service_gamma.log`
   These files contain log entries with UNIX timestamps at the beginning of each line (e.g., `1690001000 [INFO] Payload chunk...`). 
   You must combine all entries from these three files and sort them chronologically by the timestamp to reconstruct the exact sequence of events. Save the merged and sorted output to `/home/user/reconstructed.log`.

2. **Concurrency Debugging & Convergence Repair:**
   The attackers left behind the source code for their payload decoder: `/home/user/decoder.c`. 
   This C program reads `/home/user/reconstructed.log`, spins up multiple POSIX threads to parse the entries, and aggregates a checksum in a shared global variable to verify the payload.
   However, the program currently fails to converge on the correct final checksum because of a classic race condition in how the threads update the global variable.
   You must:
   - Identify the race condition in `/home/user/decoder.c`.
   - Fix the code (e.g., by adding a proper mutex lock around the critical section).
   - Compile the fixed code into an executable at `/home/user/decoder`.
   - When run against `/home/user/reconstructed.log`, the fixed program will successfully converge and print a final success key.

3. **System Call Tracing:**
   Once the `decoder` program successfully converges on the correct checksum, it briefly attempts to interact with the filesystem (a hidden persistence mechanism) before exiting. This interaction is not visible in standard output.
   Use system call tracing (e.g., `strace`) on your fixed binary to discover the exact absolute file path the program attempts to `openat` or `open` immediately after successful convergence.

4. **Reporting:**
   Create a JSON report at `/home/user/investigation.json` with the following exact keys and your discovered values:
   ```json
   {
     "reconstructed_lines": <integer, total number of lines in reconstructed.log>,
     "convergence_key": "<string, the exact success key printed to stdout by the fixed binary>",
     "suspicious_file": "<string, the absolute file path the binary attempted to open upon success>"
   }
   ```