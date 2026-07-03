You are acting as a network security engineer. We have intercepted a batch of authentication requests that we suspect contain intrusion attempts. We have a skeletal C++ log analysis tool, but it is incomplete.

Your task is to fix the C++ tool to correctly perform cryptographic checksum verification and pattern matching to identify the source IPs of the attackers.

The workspace is located at `/home/user/traffic_inspector/`.

Inside this directory, you will find:
1. `auth_logs.txt` - A pipe-separated log file of intercepted authentication requests. The format is: `IP | Username | AuthToken | SHA256(AuthToken)`
2. `inspector.cpp` - A partially written C++ program.
3. `Makefile` - Build instructions.

You need to modify `inspector.cpp` to do the following for each line in `auth_logs.txt`:
1. Parse the line.
2. Compute the SHA-256 hash of the `AuthToken` (using OpenSSL).
3. Compare your computed hash against the provided `SHA256(AuthToken)` in the log. If they do NOT match, the packet was tampered with in transit and should be ignored entirely (do not flag it).
4. If the hash matches (valid authentication flow), check if the `AuthToken` contains the exact substring `EXPLOIT_PATTERN_X99` (intrusion detection).
5. If the hash is valid AND the intrusion pattern is found, append the attacker's `IP` to `/home/user/traffic_inspector/flagged_ips.log` (one IP per line).

Ensure that your `Makefile` correctly links the necessary OpenSSL libraries (`-lssl -lcrypto`).
Compile your program by running `make` and execute it to generate the `/home/user/traffic_inspector/flagged_ips.log` file.