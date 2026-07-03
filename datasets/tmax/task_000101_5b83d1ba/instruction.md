You are a storage administrator managing a massive migration of legacy disk backups to a new structured log system. 

We have a proprietary backup metadata format scattered across our disks. Previously, we used a C utility to read these files, which is available as a stripped binary at `/app/legacy_parser`. If you run `/app/legacy_parser <input_file>`, it parses the binary backup file and dumps a JSON representation of the metadata. 

However, we recently discovered that `legacy_parser` is highly vulnerable. It crashes on corrupted files and blindly accepts malicious path traversals (e.g., `../` in filenames), which corrupts our incremental backup database downstream.

Your task is to write a secure replacement in Go.
Create a Go program at `/home/user/converter.go`. It must accept exactly two arguments:
`go run /home/user/converter.go <input_file> <output_json_file>`

Your Go program must:
1. Reverse-engineer the binary format by observing the behavior of `/app/legacy_parser` on some sample files (you can generate your own test files or explore the provided corpora).
2. Read the `<input_file>`.
3. Validate the file strictly. You must reject the file (exit with a non-zero status code and ensure the output file is NOT created) if:
   - The magic bytes or structure is invalid.
   - Any declared lengths would read past the end of the file.
   - Any extracted filename contains directory traversal sequences (`..`, `/`, `\`).
4. If the file is perfectly valid, convert the parsed metadata to a JSON array exactly matching the schema produced by `/app/legacy_parser`.
5. Write the resulting JSON to `<output_json_file>` using an **atomic write** (write to a temporary file in the same directory, then rename it) to prevent partial writes if the disk fills up. 

To help you test, we have provided two directories:
- `/app/corpus/clean/` : Contains valid backup blobs. Your program must successfully convert 100% of these.
- `/app/corpus/evil/` : Contains corrupted or malicious blobs. Your program must reject 100% of these without crashing.

Write the code and ensure it is saved at `/home/user/converter.go`.