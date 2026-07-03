You are acting as a storage administrator handling a security audit on a recently suspected "Zip Slip" vulnerability during an archive extraction process. Some files may have attempted to extract outside their designated safe base directory.

Your task is to write a C++ program that interprets the configuration, parses the extraction logs, identifies malicious path traversals, calculates checksums for the quarantined malicious payloads, and outputs a threat manifest.

Here are the details of the system state:
1. **Configuration File**: `/home/user/config.json`
   This JSON file contains a single key `"base_dir"`. This is the safe absolute directory path where files were supposed to be extracted.

2. **Extraction Log**: `/home/user/extraction.log`
   This is a multi-line log file where each entry is separated by a blank line. Each entry has the following format:
   ```
   Record ID: <integer>
   Path: <string>
   Size: <integer>
   ```
   The `Path` is the raw, un-normalized path where the archive tried to write the file. 

3. **Quarantine Directory**: `/home/user/quarantine/`
   The extraction system intercepted the files and placed their actual contents in this directory. The files are named `<Record ID>.dat` (e.g., `101.dat`).

**Your Objectives:**
1. Write a C++17 program (e.g., `/home/user/audit.cpp`) and compile it.
2. The program must parse `/home/user/config.json` to determine the `base_dir`.
3. The program must parse `/home/user/extraction.log`.
4. For each record, normalize the `Path` (resolving any `.` and `..` segments). 
5. Determine if the normalized path escapes the `base_dir`. A path escapes if it does not strictly fall within the `base_dir` directory tree.
6. For every record that *escapes* the base directory, calculate the SHA-256 checksum of its corresponding quarantined file in `/home/user/quarantine/`.
7. Generate a CSV manifest of the escaping files at `/home/user/threat_manifest.csv`.

**Manifest Format:**
The file `/home/user/threat_manifest.csv` must use the following strict CSV format (no headers):
`<Record ID>,<Normalized Path>,<SHA256 Checksum>`

Example line:
`102,/home/user/.ssh/id_rsa,e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

You may use standard C++17 libraries (like `<filesystem>`) and invoke external shell commands (like `sha256sum`) from within your C++ code if you prefer not to implement cryptographic hashing from scratch. Complete the task by executing your compiled C++ program so that the manifest is created.