You are a backup administrator recovering data from an old archiving system. We have discovered that the legacy backup system occasionally generated malicious archives with "Zip Slip" path traversal vulnerabilities (e.g., containing file paths like `../../etc/passwd` or `/root/hidden_overwrite.txt`) due to a compromised node. 

We need to recover a critical audio voicemail and its metadata from one of these compromised incremental backups, but we cannot risk using standard extraction tools directly.

Your task is to write a custom secure extraction tool in **Rust** and then recover the contents of the archive.

Here are the requirements:

1. **Secure Extraction Tool (Rust):**
   - Create a Rust project (using Cargo) in `/home/user/extractor`.
   - The program must read a `.tar.gz` archive and extract its contents into a specified target directory.
   - **Archive Integrity & Zip Slip Protection:** The program must inspect every file path in the archive. If a path is absolute, or contains `..` components that would cause it to escape the target directory, the program MUST skip extracting that file.
   - For every skipped malicious or escaping file, append its exact archive path to `/home/user/skipped.log`.
   - For every safely extracted file, print its name to stdout.
   - You may use standard crates like `tar` and `flate2`.

2. **Data Recovery:**
   - Compile and use your Rust tool to extract `/app/backup.tar.gz` into `/home/user/extracted/`.
   - The archive contains a structured metadata file, a compressed stream, some malicious payloads, and a target audio file named `voicemail.wav`.

3. **Audio Processing:**
   - Once safely extracted, you will find `voicemail.wav` in the extraction directory.
   - You must transcribe the spoken content of this audio file. You may install and use any tools you prefer (e.g., Python's `openai-whisper`, `ffmpeg`, etc.) to transcribe it.
   - Save the raw text transcript of the audio to `/home/user/transcript.txt`.

Ensure your Rust tool is robust and accurately prevents any file from being written outside `/home/user/extracted/`. The final transcript must be as accurate as possible, as it will be evaluated against a quantitative metric (Word Error Rate).