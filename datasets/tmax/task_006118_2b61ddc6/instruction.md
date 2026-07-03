You are tasked with building a secure artifact curation daemon for our build system. 

Raw build artifacts are deposited as `.zip` files into an incoming directory. However, we have identified a security risk: some external builds contain "Zip Slip" vulnerabilities—maliciously crafted zip archives with file paths containing directory traversal characters (e.g., `../`) or absolute paths (e.g., `/etc/passwd`) intended to overwrite system files upon extraction.

You need to write a Python script, `/home/user/curator.py`, that acts as an artifact manager. 

The script must fulfill the following requirements:
1. **File Watching & Lifecycle:** Continuously monitor the directory `/home/user/incoming/` for new files. If a file named exactly `SHUTDOWN` appears in this directory, the script must exit cleanly with status code 0.
2. **Extraction & Filtering:** When a `.zip` file is detected:
   - Identify safe files: paths that do NOT contain `..` and do NOT start with `/`.
   - Identify malicious files: paths that contain `..` or start with `/`.
   - Extract ONLY the safe files into a temporary directory, preserving their internal directory structure.
3. **Archive Creation & Atomic Writes:**
   - Repackage the safe files into a new `.tar.gz` archive. 
   - The new archive must be placed in `/home/user/curated/` and named `<original_filename_without_ext>.tar.gz` (e.g., `app_build.zip` becomes `app_build.tar.gz`).
   - You **must** use an atomic write pattern: write the `.tar.gz` to a temporary hidden file in `/home/user/curated/` (e.g., `.app_build.tar.gz.tmp`), and then rename it to the final target name.
   - Delete the original `.zip` file from `/home/user/incoming/` after successful curation.
4. **Logging (Standard Stream Redirection):**
   - For every processed `.zip` file, print exactly one line to Standard Output (`stdout`) in the following format:
     `Processed <filename>: <safe_count> safe, <malicious_count> malicious`
     (Example: `Processed artifact.zip: 3 safe, 1 malicious`)

Once your script is written, run it in the background using `python3 /home/user/curator.py > /home/user/logs/curator.log 2>&1 &`. Ensure all necessary directories exist before starting. 

Do not use third-party libraries outside the Python standard library. Wait for the background process to start before concluding your turn.