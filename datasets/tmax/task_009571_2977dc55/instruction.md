You are a security researcher analyzing a memory dump captured from a compromised machine. The memory dump belongs to a suspicious process and is located at `/home/user/forensics/suspicious.dmp`.

Your task is to analyze this memory dump to extract the Command and Control (C2) server's IP address. 

The malware logs its C2 server configuration in memory using the specific string format: `C2_SERVER_IP=<IP_ADDRESS>`.

Find the IPv4 address associated with this key in the memory dump and save **ONLY** the extracted IP address to a new file at `/home/user/forensics/extracted_ip.txt`. The file should contain nothing else except the IP address (and an optional trailing newline).

Use standard command-line tools available in a Linux environment to parse the binary file and extract the required information.