I received a project archive `/home/user/project_files.tar` from an untrusted third-party vendor. I suspect it might contain a "Zip Slip" vulnerability—maliciously crafted file paths designed to overwrite files outside the extraction directory (e.g., using absolute paths or directory traversal sequences like `../`).

I need you to safely parse, filter, and extract data from this archive using Bash.

Please perform the following steps:
1. **Analyze the Archive:** Write a bash command or script to inspect the contents of `/home/user/project_files.tar` without extracting it. 
2. **Identify Unsafe Paths:** Identify any file paths in the archive that are "unsafe". A path is considered unsafe if:
   - It is an absolute path (starts with `/`).
   - When logically normalized, it attempts to traverse above the base extraction directory (e.g., `../outside.txt` or `docs/../../outside.txt`).
   *(Note: A path like `docs/../docs/safe.txt` is safe because it resolves safely within the base directory).*
3. **Log Unsafe Paths:** Write the exact, original unsafe path strings from the archive into `/home/user/unsafe_paths.log`, one per line, sorted alphabetically.
4. **Safe Extraction:** Extract *only* the safe files from the tarball into the directory `/home/user/safe_extraction/`. Maintain their internal directory structure as defined in the archive (ignoring any GNU tar warnings about stripping `../` during your analysis, you must strictly extract only the files you deemed safe).
5. **Parse Logs:** Find all `.log` files within `/home/user/safe_extraction/`. Using `sed` or `awk`, extract any line that begins exactly with the word `ERROR` (case-sensitive) and save these lines to `/home/user/error_summary.txt`.

Ensure your final directories and files match these exact paths and formats so my automated security audit tools can verify your work.