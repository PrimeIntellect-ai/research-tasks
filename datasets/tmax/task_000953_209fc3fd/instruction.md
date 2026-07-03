You are an incoming Backup Administrator for a critical data infrastructure team. Your predecessor left abruptly, leaving behind a backlog of unverified backup archives and a voicemail containing the encryption signature password.

Your task is to write a Python CLI tool that safely filters, verifies, and organizes a set of `.tar` archive files without falling victim to malicious archives (e.g., zip-bombs, tar-slips).

First, retrieve the backup signature password by listening to or transcribing the audio file left by your predecessor at `/app/voicemail.wav`. You will need to install an audio transcription tool (like `whisper-net` or use the OpenAI API if you have a key, or standard open-source transcription tools like `whisper.cpp` or `ffmpeg` + `vosk`) to find out the passphrase spoken in the audio.

Next, write a Python script at `/home/user/archive_filter.py` with the following CLI signature:
`python3 /home/user/archive_filter.py --input <input_directory> --output <output_directory> --password "<spoken_password>"`

Your script must process all `.tar` files in the `<input_directory>` and apply the following rules:
1. **Signature Verification (Streaming/Mmap I/O)**: Use memory-mapped I/O (`mmap`) or efficient tail-seeking to read exactly the last 20 bytes of each archive. The archive is only valid if it ends with the exact string `BKP_` followed immediately by the spoken password (ignoring spaces/punctuation from the transcript, e.g., if the audio says "password is red apple", the signature to check is `BKP_redapple`).
2. **Archive Integrity & Security**: Analyze the tar headers without extracting the archive. Reject any archive that exhibits "tar-slip" vulnerabilities (e.g., contains absolute paths, paths with `../` traversing upwards, or symlinks/hardlinks pointing to targets outside the archive's internal root).
3. **Link Management**: If an archive passes both the signature and security checks, it is considered "Clean". You must create a **hard link** to this archive in the `<output_directory>`. Do not copy the file; use hard links to save disk space. If it fails *any* check, ignore it (do not link it).

To help you develop and test your script, there are two directories provided:
- `/app/corpora/clean/`: Contains valid, well-formed `.tar` files with the correct signature.
- `/app/corpora/evil/`: Contains malicious archives (directory traversal, absolute paths, cyclic symlinks) or archives with missing/corrupted EOF signatures.

Your final script will be tested automatically by running it against isolated hidden test sets identical in structure to these corpora. Make sure your script handles errors gracefully and correctly isolates safe backups from dangerous or corrupted ones.