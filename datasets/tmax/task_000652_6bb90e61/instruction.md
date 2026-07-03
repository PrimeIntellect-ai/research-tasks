You are assisting a security auditing team with building an automated binary inspection tool. 

The lead security auditor has left a voice memo detailing the precise logic, offsets, and output formats required for the new custom inspection utility. This memo is located at `/app/audit_memo.wav`.

Your task is to:
1. Transcribe or analyze the audio file `/app/audit_memo.wav` to recover the hidden business logic and rules for the auditing tool.
2. Implement this logic in a C program located at `/home/user/auditor.c`.
3. Compile your program to `/home/user/auditor` (e.g., using `gcc -O2 /home/user/auditor.c -o /home/user/auditor`).

Constraints for the C program:
- It must read exactly 32 bytes of binary data from standard input (`stdin`).
- It must apply the binary format analysis, permission checks, and payload signature matching exactly as described in the voice memo.
- It must print ONLY the exact alert strings specified in the audio, followed by a newline (`\n`), and then exit with code 0.
- Do not add any extra debugging output to standard output. 

An automated verification system will run your compiled binary against thousands of random 32-byte inputs and compare its output bit-for-bit against a reference oracle to ensure the security auditing logic is strictly equivalent.