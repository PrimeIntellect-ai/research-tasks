You are a network engineer auditing a Linux server for a rogue service that is known to leak its TLS private key passphrase in its command-line arguments (visible via `/proc`). 

We have captured an image of the architecture diagram at `/app/network_diagram.png`. This image contains the specific TCP port number the rogue service is listening on.

Your task is to write a C program that can dynamically find this leaked credential for any given port. 
1. Examine `/app/network_diagram.png` to find the target port.
2. Write a C program at `/home/user/finder.c` that takes a single command-line argument (a TCP port number in decimal). The program must:
   - Parse `/proc/net/tcp` to find the inode of the socket in the `LISTEN` state (state `0A`) on that specific port.
   - Scan through `/proc/[pid]/fd/` for all running processes to find the PID that holds a file descriptor pointing to `socket:[<inode>]`.
   - Read `/proc/[pid]/cmdline` for that process.
   - Extract and print ONLY the value associated with the `--passphrase=` argument (e.g., if the cmdline has `--passphrase=Secret123`, print `Secret123` to standard output without a newline).
3. Compile your program to `/home/user/finder` using `gcc`.
4. Create a bash script at `/home/user/firewall_rule.sh` that echoes the exact `iptables` command required to drop all incoming TCP traffic to the port found in the image.

Ensure your C code is robust and handles standard `/proc` formatting.