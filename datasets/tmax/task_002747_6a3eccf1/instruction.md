You are a storage administrator managing a high-throughput file upload service. Users upload custom "SAR" (Storage Archive) files. We recently discovered that our proprietary extraction tool, located at `/app/sarextract`, contains a "zip slip" vulnerability: it blindly extracts files to absolute paths or resolves `../` sequences, allowing malicious archives to overwrite arbitrary files outside the target extraction directory.

Because `/app/sarextract` is a proprietary, stripped binary, we cannot patch it directly. Instead, you must create a pre-extraction security filter.

Your task is to write a script at `/home/user/detector.py` that takes a single command-line argument (the absolute path to a SAR archive) and analyzes its binary structure to read the filenames within.

Your script must:
1. Parse the SAR archive header and file entries to extract all intended extraction paths. You will need to reverse-engineer the simple binary format by examining `/app/sarextract` and the example files provided in `/app/corpus/clean/` (safe archives) and `/app/corpus/evil/` (malicious archives).
2. Determine if the archive is safe. An archive is malicious if ANY file path within it:
   - Starts with a forward slash `/` (absolute path)
   - Contains the exact directory component `..` (e.g., `../foo`, `foo/../bar`, `foo/..`)
3. If the archive is safe, print exactly `ACCEPT` to standard output and exit with code 0.
4. If the archive is malicious, print exactly `REJECT` to standard output and exit with code 1.
5. In both cases, append a log entry to `/home/user/scan_log.txt` in the exact format: `[PATH] [DECISION]`, where `[PATH]` is the archive's absolute path and `[DECISION]` is either `ACCEPT` or `REJECT`. 

**Critical Requirement:** The storage service processes uploads concurrently. The verifier will invoke your script on hundreds of archives simultaneously. You **must** implement proper file locking (e.g., `fcntl.flock` in Python) when appending to `/home/user/scan_log.txt` to prevent log corruption.

You may use Python, Perl, Ruby, or bash.