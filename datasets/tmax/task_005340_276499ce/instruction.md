You are a storage administrator working on consolidating old backups. You've discovered that some legacy backup pipelines were compromised and contain malicious nested archives designed to overwrite system files via path traversal attacks (also known as "Zip Slip").

Your task is to write a C++ tool that safely processes these legacy tarball archives, extracts the legitimate files, handles nested archives, and generates a cryptographic manifest, all while actively blocking path traversal attacks.

Requirements for your tool (`/home/user/safe_extractor.cpp`):
1. **Archive Processing**: Read an uncompressed tar archive from `/home/user/input.tar`. You may use `libarchive` (which you can install via `apt-get`).
2. **Path Traversal Protection (Zip Slip)**: 
   - Analyze the path of every file in the archive. 
   - Reject and skip any file whose path is absolute (starts with `/`) or contains path traversal sequences (`../` or ending in `..`).
3. **Nested Archives**: If a safe file inside the archive is itself an uncompressed tar archive (ends with `.tar`), your tool must recursively extract its safe contents as well. Extract nested contents directly into the target extraction directory, preserving their internal relative paths.
4. **Extraction**: All safe files (including those from nested archives) must be extracted to `/home/user/extracted/`.
5. **Manifest Generation**: After extraction, compute the SHA-256 hash of every safely extracted file. Write a manifest to `/home/user/manifest.txt`.
   - Each line in the manifest must strictly follow the format: `<lowercase_hex_sha256>  <relative_path_from_extraction_dir>`
   - Example line: `d2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26  reports/q1.txt`
   - Sort the manifest lines alphabetically by the file path.

Compile your program as `safe_extractor` and run it. The final system state must have the sanitized files in `/home/user/extracted/` and the accurate `/home/user/manifest.txt`.

Note: You have root privileges via `sudo` to install any necessary development libraries (e.g., `libarchive-dev`, `libssl-dev`).