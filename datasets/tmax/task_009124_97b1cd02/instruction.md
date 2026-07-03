You are an artifact manager tasked with curating a local binary and text repository. The repository is located at `/home/user/repo` and has accumulated various text-based configuration and documentation files over time. Some directories contain symlinks, and due to a previous backup error, there is a known circular symlink (an infinite loop) inside the repository.

You need to write and execute a Python script that performs the following curation steps:

1. **Configuration File Interpretation:**
   Read the configuration file at `/home/user/curator.json`. It contains a JSON object with three keys:
   - `extensions`: A list of file extensions to process (e.g., `[".txt", ".conf"]`).
   - `source_encoding`: The current character encoding of these files (e.g., `"windows-1252"`).
   - `target_encoding`: The encoding they must be converted to (e.g., `"utf-8"`).

2. **Traversal and Loop Prevention:**
   Traverse the `/home/user/repo` directory recursively to find all files matching the given extensions. You MUST follow directory symlinks during your traversal to find files in linked directories, but you must implement a mechanism to detect and prevent infinite loops caused by circular symlinks.

3. **Character Encoding Conversion & Atomic Writes:**
   For each matching file found:
   - Read the file using the `source_encoding`.
   - Convert and write the content back using the `target_encoding`.
   - The write operation **must be atomic**. You must write the new content to a temporary file in the same directory first, and then replace the original file with the temporary file.

4. **Manifest and Checksum Generation:**
   After converting a file, calculate the SHA-256 checksum of its new (target encoded) contents. 
   Generate a manifest file at `/home/user/manifest.json`. This file must be a valid JSON dictionary where the keys are the file paths relative to `/home/user/repo` (e.g., `"docs/readme.txt"`) and the values are the corresponding lowercase hex-encoded SHA-256 checksums. Only include files that were successfully processed. Do not duplicate files in the manifest if they were encountered multiple times via symlinks (use the first encountered relative path, or just ensure each unique physical file is processed and recorded once).

Write the script, run it, and ensure `/home/user/manifest.json` is generated correctly.