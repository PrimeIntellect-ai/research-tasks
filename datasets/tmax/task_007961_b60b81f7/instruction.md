I am a DevOps engineer investigating a security incident, and I need help debugging a custom forensic log parser.

I wrote a small C utility located at `/home/user/forensics/parser.c` to extract source IP addresses from our custom firewall logs. It reads a log file and writes the extracted IPs to `parsed_ips.txt` in the current directory. 

However, when I run it against the latest log file at `/home/user/forensics/auth.log`, the program crashes (Segmentation fault / stack smashing detected) before finishing, and I suspect there is an off-by-one error or boundary condition in the format parsing logic. I know that one of the logs contains a malformed IP address that is slightly too long, which might be triggering an edge case.

Your task:
1. Review the codebase in `/home/user/forensics/parser.c`.
2. Identify and fix the boundary condition / off-by-one error preventing the program from safely handling edge-case malformed IP addresses. Ensure that if an IP address string exceeds the maximum valid IPv4 length (15 characters), the parser safely truncates it at 15 characters and null-terminates the string without overflowing the stack buffer.
3. Recompile the program using `gcc /home/user/forensics/parser.c -o /home/user/forensics/parser`.
4. Run the compiled executable against `/home/user/forensics/auth.log` from the `/home/user/forensics` directory.
5. Ensure the final output is successfully written to `/home/user/forensics/parsed_ips.txt`.

Do not change the output format or the name of the output file. Just fix the memory corruption bug so the script can process the entire file and extract the IPs.