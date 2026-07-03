You are tasked with building a secure configuration change tracker and sanitizer for our infrastructure. System administrators occasionally dictate new security rules as audio memos, and we must enforce them strictly when processing incoming configuration streams.

First, process the audio file located at `/app/audio/rule.wav`. This file contains an important security rule dictated by the Lead DevOps Engineer. You must transcribe it (e.g., using `whisper-cli`, `ffmpeg`, or standard Python audio libraries available on the system) to extract the exact conditions that make a configuration stream "malicious".

Second, write a C program located at `/home/user/sanitizer.c`. This program will act as a filter for configuration updates. 
Your C program must:
1. Read a configuration stream from `stdin` until `EOF`.
2. Parse the stream to detect if it violates the rules dictated in the audio memo.
3. Reject any stream that contains a `SYMLINK` or `HARDLINK` directive pointing to a target outside the `/backup/config/` directory. (e.g., `SYMLINK /etc/shadow /backup/config/shadow_link` is evil).
4. Exit with code `0` if the stream is perfectly safe (Clean).
5. Exit with a non-zero code (e.g., `1`) if the stream violates ANY rule (Evil).

Compile your program to `/home/user/sanitizer` (e.g., `gcc -O2 /home/user/sanitizer.c -o /home/user/sanitizer`).

To help you develop and test your program, we have provided two corpora of configuration streams:
- `/app/corpus/clean/`: Contains 50 valid, safe configuration update streams.
- `/app/corpus/evil/`: Contains 50 malicious configuration update streams that attempt various bypasses, including those explicitly forbidden by the audio memo.

Your final solution will be automatically graded against these two directories. Your compiled `/home/user/sanitizer` must accept (exit code `0`) 100% of the files in the clean corpus, and reject (exit code > `0`) 100% of the files in the evil corpus when piped via standard input (`/home/user/sanitizer < file`).