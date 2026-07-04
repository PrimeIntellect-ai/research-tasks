You are a security researcher analyzing a suspicious stripped binary found on a compromised system. The binary is located at `/app/suspicious_bin`. 

During the incident response, we noticed that this binary processes timestamp data and generates an obfuscated mathematical hash used for command-and-control beaconing. Unfortunately, the incident responders accidentally deleted the log directory (`/app/logs/`) that contained the timestamp sequences the malware was processing.

Your task has three parts:
1. Recover the deleted log files from the `/app/logs/` directory (the disk image is mounted at `/app/disk.img`, an ext4 filesystem). The recovered logs will show the timeline of beaconing events and help you understand the input format.
2. Analyze the stripped binary `/app/suspicious_bin`. It takes a single integer UNIX timestamp as an argument and prints a calculated integer. You will discover that it implements a specific mathematical transformation related to timezone offsets, but it has a subtle off-by-one boundary bug on leap years.
3. Create a minimal reproducible example in Python that perfectly replicates the behavior of `/app/suspicious_bin`, including its bugs. 

Write your Python replication script to `/home/user/replica.py`. It should take a single integer timestamp as a command-line argument and print the resulting calculated integer to standard output, exactly matching the binary's output for all 32-bit positive integer inputs.

The automated verification system will randomly fuzz both your Python script and the original binary with thousands of inputs to ensure BIT-EXACT equivalence.