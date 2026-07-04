You are tasked with fixing a critical vulnerability in our configuration management system and building a secure configuration processor. Our system processes configuration bundles (Zip archives containing JSON configs, WAL logs, and occasional ELF binaries) uploaded by users. 

Recently, a security audit found a "Zip Slip" vulnerability in our internal archiving library, allowing malicious archives to overwrite files outside the intended extraction directory.

**Phase 1: Fix the Vendored Package**
We have an internal package `securezip` vendored at `/app/vendor/securezip`. 
The function `SanitizePath(dest, filename string) (string, error)` in `/app/vendor/securezip/utils.go` is currently a stub that just returns `filepath.Join(dest, filename)` without validating if the resolved path stays within the `dest` directory.
1. Modify `/app/vendor/securezip/utils.go`.
2. Ensure `SanitizePath` securely resolves the path. If the resulting path does NOT have the `dest` directory as its base (indicating a path traversal attempt), it MUST return an error containing the exact string `"zip slip detected"`.

**Phase 2: Build the Configuration Processor**
Write a Go program at `/home/user/extract_config.go`.
1. It must read a zip file stream entirely from standard input (`os.Stdin`).
2. It must clear and create the directory `/tmp/config_dest`.
3. It must use the `securezip` package to extract the archive to `/tmp/config_dest` by calling `securezip.Extract(bytes.NewReader(input), int64(len(input)), "/tmp/config_dest")`.
4. **Output Format**:
   - If extraction fails (e.g., zip slip error, invalid zip), your program must print EXACTLY: `{"error": "<error_message>"}` to standard output and exit with code 0.
   - If extraction succeeds, recursively scan `/tmp/config_dest` for any `.json` files. Parse each JSON file to ensure it is valid. Ignore invalid JSON files or files with other extensions.
   - Print a JSON object to standard output representing the valid JSON files, sorted alphabetically by their base filename:
     `{"success": true, "files": [{"name": "a.json", "size": 123}, {"name": "b.json", "size": 456}]}`
   - You must clear `/tmp/config_dest` at the end of the execution.

Your output must be absolutely deterministic. It will be verified against a reference implementation using hundreds of fuzzed inputs, including malicious archives.