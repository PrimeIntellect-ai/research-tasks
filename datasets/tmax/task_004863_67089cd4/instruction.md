You are a backup operator tasked with testing restores of our legacy system configurations. We used to rely on a proprietary tool to back up our firewall rules, port forwarding setups, and email/mailing list server configurations. 

The tool that restores these backups is a stripped Linux executable located at `/app/backup_decoder`. It reads a proprietary binary backup blob from standard input (`stdin`) and prints the decrypted, plaintext configuration data (which includes firewall commands and email server config expectations) to standard output (`stdout`). 

Unfortunately, we have lost the source code for this utility and need to migrate away from it. Your task is to reverse-engineer the `/app/backup_decoder` binary and write a pure Python 3 script at `/home/user/decoder.py` that behaves **exactly** identically.

Your script must:
1. Read bytes from standard input (`sys.stdin.buffer`).
2. Implement the exact same decoding logic as `/app/backup_decoder`.
3. Output the exact same bytes to standard output (`sys.stdout.buffer`).
4. Replicate the exit codes of the original binary (e.g., if the backup is corrupt or invalid).

You may use standard reverse-engineering tools (`objdump`, `gdb`, `strings`, `ltrace`, `strace`, etc.) available on the system to analyze `/app/backup_decoder`. We will test your script by feeding thousands of random, fuzzed backup blobs to both the original binary and your Python script and asserting that the standard output, standard error, and exit codes match bit-for-bit.

Save your final Python script precisely at `/home/user/decoder.py`.