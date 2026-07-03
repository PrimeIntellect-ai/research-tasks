You are managing an artifact curation pipeline for a secure binary repository. The system receives ELF binaries via a web API, but we have discovered that malicious actors are hiding destructive GCode sequences inside custom ELF sections to compromise our robotic assembly nodes.

Currently, the pipeline consists of three services running on the server:
1. An Nginx reverse proxy (listening on port 8080).
2. A Flask submission API (running on port 5000) located at `/home/user/services/api/`.
3. A Redis artifact metadata store (running on port 6379).

Your task is to build a C++ sanitizer, configure it, and integrate it into the pipeline to block malicious uploads.

Step 1: Build the ELF & GCode Sanitizer
Write a C++ program at `/home/user/sanitizer/elf_sanitizer.cpp` and compile it to `/home/user/sanitizer/elf_sanitizer`. 
The program must take a directory path as a command-line argument. It should recursively traverse the directory, find all files with a `.elf` extension, and parse their ELF headers. 
For each ELF file:
- Check if it contains a section named `.cnc_gcode`.
- If the section exists, read its contents as plain text GCode.
- Parse the GCode lines. A file is considered "evil" if any `G0` or `G1` command contains a negative Z-axis movement (e.g., `Z-1.5`, `Z-0.1`). Clean files either lack this section or only contain Z values >= 0.0.
- The program must exit with code 1 if ANY evil files are found in the directory, and exit with code 0 if all files are clean.
- Ensure your code handles standard 64-bit ELF formats (`ELF64`).

Step 2: Evaluate Against the Corpora
There are two directories containing test corpora:
- `/home/user/corpora/clean/`: Contains 50 clean ELF binaries.
- `/home/user/corpora/evil/`: Contains 50 evil ELF binaries with negative Z-axis GCode payloads.
Ensure your C++ sanitizer correctly rejects 100% of the evil corpus and accepts 100% of the clean corpus. 

Step 3: Integrate with the Services
The Flask application at `/home/user/services/api/app.py` currently accepts uploads to `/upload` and saves them to `/home/user/staging/`. It then directly registers them in Redis.
Modify the Flask application so that before saving to Redis, it invokes your `/home/user/sanitizer/elf_sanitizer` on the `/home/user/staging/` directory. If the sanitizer exits with code 1, the Flask app must return an HTTP 403 Forbidden status and delete the offending file. If it returns 0, the process should continue as normal.

Restart the Flask and Nginx services as necessary to apply your changes. A verification script will test the end-to-end flow by uploading a mix of clean and evil payloads via port 8080 and verifying that only clean artifacts end up in Redis.