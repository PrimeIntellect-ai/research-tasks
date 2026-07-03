You are acting as an artifact manager for a local binary repository. We have received some new binary artifacts in a staging directory, and they need to be processed, chunked, and cataloged into our repository format.

Your task is to process all `.bin` files located in `/home/user/staging/` and store the results in `/home/user/repo/`.

**Artifact Format:**
Each `.bin` file starts with a 16-byte header, followed immediately by the binary payload.
The header consists of:
- **Bytes 0-3:** A 4-byte ASCII string representing the "Magic Number".
- **Bytes 4-7:** A 4-byte unsigned little-endian integer representing the "Version".
- **Bytes 8-15:** 8 bytes of reserved padding (ignore these).

**Processing Requirements:**
For every `.bin` file in `/home/user/staging/` (e.g., `app_v1.bin`):
1. Extract the Magic Number and Version from the header.
2. Extract the actual payload (everything after the 16-byte header).
3. Compute the SHA256 checksum of the *payload* (not the whole file).
4. Split the payload into 100KB (102,400 bytes) chunks.
5. Store the chunks in a dedicated directory for the artifact: `/home/user/repo/<basename>/` (e.g., `/home/user/repo/app_v1/`).
6. Name the chunks with a `chunk_` prefix and a 2-digit numeric suffix starting from `00` (e.g., `chunk_00`, `chunk_01`, `chunk_02`).

**Manifest Generation:**
Once all artifacts are processed, generate a single JSON manifest file at `/home/user/repo/manifest.json`. The JSON must precisely follow this structure:

```json
{
  "app_v1": {
    "magic": "DATA",
    "version": 3,
    "payload_sha256": "a1b2c3d4...",
    "chunks": [
      "chunk_00",
      "chunk_01"
    ]
  },
  "other_artifact": {
    ...
  }
}
```

**Constraints:**
- Do not include the `.bin` extension in the manifest keys or folder names.
- Ensure the chunk files contain exactly the payload data without the 16-byte header.
- You may use any scripting language (Python, bash, etc.) available in the environment to accomplish this.