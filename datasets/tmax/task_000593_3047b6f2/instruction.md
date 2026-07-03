You are tasked with building a secure configuration ingest tool in Go that tracks and processes incoming configuration archives.

We have an incoming configuration archive located at `/home/user/incoming/update.zip`. We need to extract it, process its contents, and generate a manifest of the changes. However, we suspect that some archives might be maliciously crafted to overwrite files outside the intended target directory (a vulnerability known as "zip slip"). Furthermore, the incoming configuration files are legacy systems that use the `Windows-1252` character encoding, but our modern systems require strict `UTF-8`.

Your objective is to write a Go program at `/home/user/config_manager/ingest.go` that does the following:

1. **Initialization:** Initialize a Go module in `/home/user/config_manager`. You may download any necessary standard or popular third-party Go packages (e.g., `golang.org/x/text/...`).
2. **Safe Extraction:** The program must take two command-line arguments: the path to the zip file, and the target extraction directory. When you run it, you will pass `/home/user/incoming/update.zip` and `/home/user/config_target`.
   - The program must safely extract the contents of the zip file into the target directory.
   - **Crucial Security Requirement:** It must prevent "zip slip" attacks. If any file path within the zip archive resolves to a location outside the target extraction directory, your program must **skip** extracting that specific file and continue with the rest. Do not error out completely; just ignore the malicious entries.
3. **Encoding Conversion & Recursive Traversal:** After extraction, the program must recursively traverse the target extraction directory.
   - For every file found, read its contents, decode it from `Windows-1252`, and re-encode it as `UTF-8`.
   - Overwrite the extracted file with the new `UTF-8` content.
4. **Manifest Generation:** As you process the files, calculate the `SHA-256` checksum of the newly converted `UTF-8` contents.
   - The program must generate a JSON manifest file at `/home/user/manifest.json`.
   - The manifest must be a flat JSON object where the keys are the relative file paths (relative to the target extraction directory, using forward slashes) and the values are the lowercase hexadecimal SHA-256 strings.

Example of expected `/home/user/manifest.json` format:
```json
{
  "server.conf": "a1b2c3d4...",
  "app/settings.txt": "e5f6g7h8..."
}
```

After writing the program, build and run it against `/home/user/incoming/update.zip` and `/home/user/config_target`. Verify that the manifest is created and that no files were extracted outside the target directory.