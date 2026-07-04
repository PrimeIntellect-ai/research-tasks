You are an AI assistant helping a technical writer organize a set of legacy documentation files. 

The writer has an archive of old documentation located at `/home/user/legacy_archive.tar`. Inside this tar archive is a nested directory structure containing text files (`.txt`). These files are currently encoded in ISO-8859-1 (Latin-1), and their filenames contain spaces.

Your task is to write and execute a Go program at `/home/user/organize.go` that performs the following workflow:

1. **Extract**: Extract the contents of `/home/user/legacy_archive.tar` to a temporary directory (e.g., `/home/user/extracted`).
2. **Process & Path Manipulation**: Find all `.txt` files within the extracted directories (including all subdirectories). For each file, determine its new path by flattening the directory structure (placing all files directly into `/home/user/processed/`) and replacing any spaces in the filename with underscores (`_`).
3. **Character Encoding Conversion**: Read the contents of each `.txt` file, convert the text from ISO-8859-1 to UTF-8, and write the converted content to the new flattened path in `/home/user/processed/`.
4. **File Locking & Logging**: As your Go program processes each file, it must append the new filename (just the base name, e.g., `file_1.txt`) followed by ` - UTF8 Converted` to a central log file at `/home/user/processed/manifest.log` (e.g., `file_1.txt - UTF8 Converted`). Because this script might run in a concurrent environment in the future, you **must** implement an exclusive file lock (e.g., using `syscall.Flock`) on `manifest.log` before appending each entry, and unlock it immediately after.
5. **Re-Archive**: Finally, use Go's `archive/zip` package (or call the `zip` command via `os/exec`) to compress the entire `/home/user/processed/` directory (including the converted `.txt` files and `manifest.log`) into a new archive located at `/home/user/final_docs.zip`.

**Requirements:**
- Do not use third-party libraries outside the standard library unless absolutely necessary (you can use `os/exec` to call system tools like `iconv`, `tar`, or `zip` if you prefer, but the logic and file locking must be orchestrated by the Go code).
- Make sure the `/home/user/processed/` directory is created before writing to it.
- Your final deliverable is the successful creation of `/home/user/final_docs.zip` and the `/home/user/processed/manifest.log` file with the correct contents.