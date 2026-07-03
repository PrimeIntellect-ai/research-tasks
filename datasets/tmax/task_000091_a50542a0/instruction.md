I need your help to organize and sanitize a large documentation repository for our new engineering manual. I'm a technical writer, and I've been handed a messy dataset containing structured documentation, domain-specific attachments (like ELF binaries and GCode snippets), and audio interviews with the engineers. 

There are two main objectives:

**1. Audio Transcription and Link Management:**
You will find an audio file at `/app/interview.wav`. This file contains an engineer dictating the exact directory structure and symlink mapping required for our documentation release. You need to transcribe this audio (you can install and use tools like `whisper` or `ffmpeg` to process it). Based on the transcript, you must organize the raw documentation files located in `/home/user/raw_docs/` into a new structure at `/home/user/organized_docs/`. The transcript will specify which files should be hard-linked or symlinked. Create an archive named `/home/user/final_docs.tar.gz` containing the `/home/user/organized_docs/` directory.

**2. Adversarial Documentation Sanitizer:**
We receive documentation submissions from external vendors, and sometimes these contain malicious or malformed files (e.g., symlink directory traversal attacks, heavily nested ZIP bombs disguised as documents, or malformed JSON/XML files). 
Write a Python script at `/home/user/sanitizer.py` that takes a directory path as a command-line argument.
The script must recursively scan the directory and:
- Return an exit code of `0` if the directory is "clean" (all JSON/XML/CSV files are well-formed, archives can be safely extracted without excessive memory/mmap usage or path traversal, and no symlinks point outside the target directory).
- Return an exit code of `1` if the directory is "evil" (contains any of the above anomalies).

Your script will be tested against two corpora of submissions. It must reject all evil submissions and accept all clean submissions.

Please complete the organization of the docs and ensure your sanitizer script is ready at `/home/user/sanitizer.py`.