You are an artifact manager tasked with curating a local binary repository. We have a repository of archived artifacts located at `/home/user/artifacts`. This directory contains several nested subdirectories with `.tar.gz` files. Unfortunately, some of the archives have been corrupted during transit.

You need to write and execute a Rust command-line tool that performs the following tasks:
1. Recursively traverses the `/home/user/artifacts` directory.
2. Identifies all `.tar.gz` files.
3. Verifies the integrity of each `.tar.gz` file. An archive is considered valid if it can be successfully decompressed (gzip) and its tar headers can be read without errors.
4. Computes the SHA-256 checksum of the original `.tar.gz` file for all *valid* archives.
5. Moves any *corrupted* `.tar.gz` files to `/home/user/quarantine/` (you should preserve their original filename; you do not need to preserve the subdirectory structure for quarantined files, just place them flat in the quarantine directory).
6. Generates a JSON manifest file at `/home/user/manifest.json` for all valid archives.

The `manifest.json` file must strictly follow this format, and the `files` array must be sorted alphabetically by the `path` to ensure deterministic output:
```json
{
  "files": [
    {
      "path": "relative/path/to/artifact.tar.gz",
      "checksum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
  ]
}
```
*Note: The `path` field must be the relative path from the `/home/user/artifacts` directory (e.g., `linux/amd64/app_v1.tar.gz`).*

Constraints & Requirements:
- You must create a new Rust project (e.g., in `/home/user/artifact_curator`) and write the code there.
- You can use external crates like `walkdir`, `sha2`, `flate2`, `tar`, `serde`, and `serde_json`.
- Compile your program in release mode and run it to perform the curation.
- The directory `/home/user/quarantine` has already been created for you.