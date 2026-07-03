You are a DevSecOps engineer tasked with enforcing policy as code for a compromised CI/CD pipeline. A recent security breach involved an attacker exfiltrating an AES decryption key through a side-channel attack, which was captured on a surveillance feed of a compromised terminal. Furthermore, the attacker poisoned our log aggregation system with obfuscated Injection and XSS payloads.

Your objective is twofold: recover the decryption key from the video artifact, use it to decrypt the captured log corpora, and then build a robust Python-based vulnerability scanner (classifier) to detect the attacker's payloads.

**Phase 1: Cryptographic Key Recovery & Integrity Verification**
1. We have captured the attacker's terminal output in a video artifact located at `/app/leak_recording.mp4`.
2. The video flashes terminal text. You must extract the frames from this video (ffmpeg is installed).
3. We have provided a helper script at `/app/extract_text.py`. You can run `python3 /app/extract_text.py <path_to_frame_image>` to reliably extract the text from a frame.
4. The attacker exfiltrated the 32-character AES-256 key in chunks. Specific frames will output text in the exact format: `KEY_CHUNK: <8_hex_chars> | CHECKSUM: <md5_hash_of_chunk>`.
5. *File Integrity Verification:* Not all chunks are valid. The attacker introduced decoy frames. You must verify the integrity of each chunk by calculating the MD5 hash of the `<8_hex_chars>` string. If the calculated MD5 matches the `<md5_hash_of_chunk>`, the chunk is valid.
6. Concatenate all valid chunks in the chronological order they appear in the video to form the 32-character hex AES decryption key.
7. Save the final 32-character string to `/home/user/recovered_key.txt`.

**Phase 2: Log Decryption**
1. The log corpora are encrypted using AES-256-CBC and are located in `/app/encrypted_corpora/evil/` and `/app/encrypted_corpora/clean/`.
2. Decrypt all files in both directories using the key you recovered. The Initialization Vector (IV) for each file is the first 16 bytes of the file. The remaining bytes are the ciphertext. There is no padding.
3. Save the decrypted files to `/home/user/decrypted_corpora/evil/` and `/home/user/decrypted_corpora/clean/`, preserving the filenames.

**Phase 3: Automated Vulnerability Scanning (Policy as Code)**
1. Write a Python script at `/home/user/log_classifier.py` that acts as a vulnerability scanner to detect XSS and SQL injection payloads.
2. The script must take exactly one argument (the file path to a log file): `python3 /home/user/log_classifier.py <file_path>`
3. The script must analyze the contents of the file.
4. If the file contains an Injection or XSS payload (the "evil" corpus), the script MUST exit with status code `1` (Reject).
5. If the file is benign and free of exploits (the "clean" corpus), the script MUST exit with status code `0` (Accept).
6. The `evil` logs contain highly obfuscated payloads (e.g., nested HTML tags, URL-encoded SQLi, whitespace manipulation), while the `clean` logs contain normal DevOps SQL queries and HTML snippets that must not trigger false positives. You will need to iteratively test and refine your classifier against the decrypted corpora in Phase 2 to ensure perfect accuracy.

Write the classifier such that it perfectly separates the evil and clean corpora.