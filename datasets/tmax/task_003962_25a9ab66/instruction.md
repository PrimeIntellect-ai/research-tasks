You are an IT backup operator testing a disaster recovery scenario. Our primary backup system has failed, and we need to restore an emergency backup payload. However, the system relies on a legacy obfuscation tool and emergency instructions left on an audio recording.

Your task is broken into three parts:

**Part 1: Re-implement the Legacy Backup Cipher**
Our backups are obfuscated using a custom C program. We have a compiled reference binary at `/app/bin/cipher_oracle` (which reads from standard input and writes to standard output), but we need the source code to audit it. 
Write a C program at `/home/user/cipher.c` and compile it to `/home/user/cipher`. 
Algorithm specification:
- Read bytes from `stdin` until EOF.
- XOR each byte with a cyclic key: the ASCII characters of the string "BACKUP" (i.e., 'B', 'A', 'C', 'K', 'U', 'P', then repeat).
- Write the resulting bytes to `stdout`.
- Exit with status code 0.
Your compiled binary `/home/user/cipher` must behave BIT-EXACTLY like `/app/bin/cipher_oracle` for any arbitrary byte stream.

**Part 2: Retrieve Emergency Routing Instructions**
Listen to or transcribe the emergency voicemail provided at `/app/voicemail_001.wav`. 
The audio contains a spoken IP address for the emergency backup gateway. 
You may use any available tool in the terminal (e.g., Python libraries, ffmpeg) to extract this information.

**Part 3: The Restore Script**
Write a bash script at `/home/user/setup_restore.sh` that automates the restore environment setup. The script must:
1. Accept exactly one command-line argument: the emergency gateway IP address obtained from the voicemail.
2. Configure network routing by adding a static route for the network `10.99.0.0/16` via the provided gateway IP address on the default interface. (Since you do not have root, print the exact `ip route add ...` command to a new file at `/home/user/route_command.txt` instead of executing it).
3. Monitor storage: Check if the `/home/user` partition has more than 1048576 KB (1 GB) of available free space (using `df`). 
4. If the space is sufficient, use your compiled `/home/user/cipher` program to deobfuscate the dummy backup payload located at `/app/backup_payload.dat` and save the output to `/home/user/restored.tar`.
5. Ensure the script is executable.

Focus on getting the C program perfectly equivalent to the oracle and the bash script functionally correct.