You are a red-team operator preparing to infiltrate a highly secure facility. The target network uses an advanced Intrusion Detection System (IDS) to monitor bash execution logs. To craft an evasion payload that won't trigger the alarms, you need to build a perfect local replica of their IDS classifier to test your payloads against. 

We have intercepted two crucial artifacts from the target:
1. `/app/surveillance.mp4`: A 24-second surveillance video (1 frame per second) of the server room. The target uses a Visible Light Communication (VLC) system. A diagnostic LED in the top-left corner of the video transmits a secret 3-character ASCII key in binary (1 second per bit, 8 bits per character, Big-Endian). A bright white LED indicates a '1', and a dark area indicates a '0'.
2. `/app/training_data.zip.enc`: An AES-256-CBC encrypted ZIP file containing a sample of the facility's bash execution logs, categorized into `evil/` (commands that triggered the IDS) and `clean/` (benign commands).

**Phase 1: Cryptanalysis & Decryption**
1. Extract the frames from `/app/surveillance.mp4` using `ffmpeg`.
2. Analyze the top-left corner (e.g., coordinates 0,0 to 10,10) of each frame to read the 24-bit binary sequence.
3. Convert the binary sequence to a 3-character ASCII string.
4. Use this 3-character string as the passphrase to decrypt `/app/training_data.zip.enc` using OpenSSL (`openssl enc -d -aes-256-cbc -pbkdf2 -in /app/training_data.zip.enc -out /tmp/training_data.zip -pass pass:<YOUR_KEY>`).
5. Unzip the file to access the `evil/` and `clean/` corpora.

**Phase 2: Vulnerability Analysis & Log Parsing**
Analyze the contents of the `evil/` and `clean/` log files. The IDS identifies malicious intent by looking for specific bash obfuscation techniques used to hide forbidden commands. Specifically, the IDS looks for the hidden presence of the strings `eval` or `nc`. The target's IDS ignores backslashes (`\`), single quotes (`'`), and double quotes (`"`) when scanning the command string. 
*Example:* `e\v'a'l` and `n"c"` are considered EVIL. `echo "hello"` is CLEAN.

**Phase 3: Secure Coding (Building the Mock IDS)**
Write a C program at `/home/user/mock_ids.c` that perfectly replicates this detection logic.
1. The program must accept a single file path as a command-line argument: `./mock_ids <path_to_payload_file>`
2. It must read the contents of the file.
3. It must strip out all `\`, `'`, and `"` characters.
4. If the resulting sanitized string contains the substring `eval` or `nc`, the program must exit with status code `1` (Reject/Evil).
5. Otherwise, it must exit with status code `0` (Preserve/Clean).
6. Compile your program to `/home/user/mock_ids` using `gcc`.

Ensure your C code compiles cleanly and accurately classifies the decrypted training corpora. The automated grading system will run your `/home/user/mock_ids` binary against a hidden adversarial corpus of evaluation payloads.