You are a Site Reliability Engineer (SRE) responsible for monitoring the uptime of our critical microservices. We have an in-house daemon written in C, `uptime_tracker`, located in the git repository at `/home/user/uptime_tracker`. Recently, the mathematical availability calculations have been wildly inaccurate, and we suspect a combination of network packet loss, a regression in the math logic, and a missing authentication secret.

Please resolve the following issues:

1. **Git Forensics & Secret Recovery**: 
   An API secret required to authenticate heartbeat packets was accidentally committed into the git repository and subsequently deleted in a later commit. Search the git history of `/home/user/uptime_tracker` to find the deleted `secret.h` file. Extract the secret string (defined as `AUTH_SECRET`) and write it exactly to `/home/user/api_secret.txt`.

2. **Network Packet Capture Analysis**:
   There is a packet capture file at `/home/user/heartbeats.pcap`. We need to know exactly how many valid heartbeat requests actually reached the server before calculating the uptime. Parse the pcap file and count the total number of HTTP GET requests made to the endpoint `/heartbeat`. Write this integer count to `/home/user/ping_count.txt`.

3. **Boundary Condition & Off-by-One Repair**:
   The primary mathematical logic in `/home/user/uptime_tracker/tracker.c` calculates a rolling average of uptime percentages. However, it crashes periodically or produces math errors due to an off-by-one boundary condition in the `calculate_rolling_average` function. Find and fix the off-by-one loop boundary bug.

4. **Intermediate State Tracing**:
   To verify the mathematical fix, instrument the `calculate_rolling_average` function in `tracker.c`. Inside the loop that calculates the sum of the uptime window, append a line to `/home/user/trace.log` for every iteration. The format MUST be exactly: `Step %d sum: %.2f\n` (where `%d` is the loop index starting at 0, and `%.2f` is the current running mathematical sum of the uptime array at that step).

5. **Build and Execute**:
   Once fixed, compile the daemon using `gcc -o tracker tracker.c` in the repository directory.
   Run the program using `./tracker`. It will read a local dummy data file, compute the correct mathematical average, write to the trace log, and exit.

**Verification criteria**:
- `/home/user/api_secret.txt` must contain the exact secret string.
- `/home/user/ping_count.txt` must contain the correct number of heartbeat packets.
- `/home/user/uptime_tracker/tracker.c` must be patched.
- `/home/user/trace.log` must contain the exact trace of intermediate mathematical sums.
- The daemon must compile and run successfully without segfaults.