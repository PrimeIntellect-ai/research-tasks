You are an AI assistant helping a DevOps team manage an artifact repository for a legacy system. 

Your environment contains a set of raw binary artifacts and a legacy text manifest. Your goal is to curate these files, chunk the large binaries for a new storage backend, generate a cryptographic manifest, and verify the integrity of the process.

Please complete the following steps:

1. **Legacy Manifest Transformation:**
   In `/home/user/artifacts/`, you will find a file named `legacy_manifest.txt`. The format is currently:
   `Artifact: <filename> | Hash: <sha1> | Date: <YYYY-MM-DD>`
   Using command-line text transformation tools (like `sed` or `awk`), convert this file into a strict CSV format in `/home/user/artifacts/legacy_manifest.csv` with the header `filename,hash,date`.
   Example output line: `app_v1.bin,a1b2c3d4e5f6,2023-01-15`

2. **Artifact Chunking and Hashing (Python):**
   Write and execute a Python script at `/home/user/curate.py`. This script must:
   - Read all `.bin` files located in `/home/user/artifacts/raw/`.
   - Split each binary into chunks of exactly 5 MiB (5,242,880 bytes). The final chunk will contain the remaining bytes.
   - Save the chunks into `/home/user/artifacts/chunked/` with the naming convention `<original_filename>.chunk.<NNN>`, where `<NNN>` is a zero-padded 3-digit integer starting from `000` (e.g., `app_v1.bin.chunk.000`).
   - Calculate the SHA-256 checksum of the original file and each individual chunk.
   - Output a JSON manifest to `/home/user/artifacts/manifest.json`. The JSON structure must match exactly:
     ```json
     {
       "filename.bin": {
         "original_sha256": "<hex_digest>",
         "chunks": {
           "filename.bin.chunk.000": "<hex_digest>",
           "filename.bin.chunk.001": "<hex_digest>"
         }
       }
     }
     ```

3. **Restoration and Verification:**
   To prove the chunking is reversible and lossless, merge the chunks of `app_v2.bin` back together into a single file at `/home/user/artifacts/restored/app_v2.bin`.
   Calculate the SHA-256 hash of this restored file and write only the hex digest to `/home/user/artifacts/restored_hash.txt`.

Ensure all directories (`chunked` and `restored`) are created if they do not exist. You may use any Python standard library modules or standard Linux utilities.