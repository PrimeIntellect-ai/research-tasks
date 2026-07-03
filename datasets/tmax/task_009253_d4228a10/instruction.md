You are an AI assistant helping a technical writer organize and sanitize incoming documentation bundles. 

The writer has received a tar archive located at `/home/user/docs_archive.tar`. This archive contains several documentation files, but it has been flagged by security because it contains "Tar Slip" payloads—malicious file paths designed to overwrite files outside the intended extraction directory (e.g., paths starting with `/` or containing `../`).

Your task is to write and execute a Python script that accomplishes the following:

1. **Sanitize and Extract:**
   - Parse `/home/user/docs_archive.tar`.
   - Identify all malicious paths (any path that is absolute, e.g., starts with `/`, or contains directory traversal components like `../`).
   - Write the exact malicious paths found in the archive to a log file at `/home/user/malicious_paths.txt`, one path per line, in the order they appear in the archive.
   - Extract **only** the safe files (those without malicious paths) into the directory `/home/user/clean_docs/` (create this directory if it doesn't exist). Maintain the internal directory structure of the safe files.

2. **Metadata Filter and Merge:**
   - After extraction, analyze the extracted safe files.
   - Find all Markdown files (`.md` extension) that have a last-modified metadata timestamp strictly newer than `2023-01-01 00:00:00 UTC`.
   - Read the text contents of these recently modified Markdown files.
   - Concatenate their contents into a single file at `/home/user/master_doc.md`. 
   - The files must be concatenated in alphabetical order of their base filenames (e.g., `a.md` before `b.md`). Separate the contents of each file with exactly one blank line.

Use standard Python 3 libraries (`tarfile`, `os`, `datetime`, etc.) to complete this task. Run your script to produce the final output files.