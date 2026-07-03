You are an artifact manager tasked with curating a binary repository that has been damaged. A rogue backup script has created an unpredictable directory structure full of recursive symlinks (symlink bombs) in the repository extract located at `/home/user/artifact_dump/`. Additionally, some artifacts have been identified as corrupted and must be purged.

Your objective is to safely extract the valid artifacts, generate a manifest, and package them into a clean, flat archive.

Perform the following steps:

1. **Extract Blacklist**: You have a large log file at `/home/user/security_logs.txt`. Scattered throughout this log are lines indicating known corrupted files, formatted exactly as: `[ERROR] Corrupt file detected - BLACKLIST_HASH: <sha256_hash>`. Extract these SHA256 hashes.
2. **Safe Traversal**: Write a Python script (e.g., `/home/user/curate.py`) that safely walks the directory tree at `/home/user/artifact_dump/`. Your script MUST handle symlinks correctly and avoid falling into infinite loops caused by the symlink bombs. 
3. **Artifact Processing**: Identify all files ending with `.bin`. For each `.bin` file:
    * Read the first 16 bytes as ASCII text. This represents the version string, padded with dashes (e.g., `VER:1.2.3-------`). Strip the trailing dashes to extract the clean version string (e.g., `VER:1.2.3`).
    * Compute the SHA256 checksum of the *entire* file (including the version header).
    * If the file's SHA256 checksum is in the blacklist from step 1, skip it entirely.
4. **Manifest Generation**: Create a JSON manifest at `/home/user/manifest.json`. The root of the JSON should be a dictionary where the keys are the SHA256 hashes of the valid (non-blacklisted) `.bin` files, and the values are objects with the following format:
    `{"version": "<clean_version_string>", "path": "<relative_path_from_artifact_dump_directory>"}`
5. **Clean Archive Creation**: Package all the valid (non-blacklisted) `.bin` files into a new gzipped tarball at `/home/user/clean_artifacts.tar.gz`. In this new tarball, ALL files must be placed at the root level (no directories) and must be renamed to `<sha256_hash>.bin`.

Do not hardcode hashes. Use standard libraries in Python. You can use standard bash tools to process the security logs if you prefer.