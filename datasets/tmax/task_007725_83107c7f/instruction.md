You are an artifact manager responsible for curating a local binary repository. You have a batch of incoming software artifacts in `/home/user/incoming/`. These artifacts are packaged as either `.tar.gz` or `.zip` archives. Each archive contains a `metadata.json` file at its root, along with various binary payloads.

Your task is to write a robust Bash script at `/home/user/curator.sh` that processes these incoming artifacts and organizes valid ones into a structured repository at `/home/user/repo/`.

The script must meet the following precise requirements:

1. **Dependency Management**: Ensure any necessary tools (like `jq`, `unzip`, `tar`, `sha256sum`) are available.
2. **Compressed Stream Processing**: Your script must iterate through all `.tar.gz` and `.zip` files in `/home/user/incoming/`. To maximize I/O efficiency, you **must NOT** extract the archives to disk. You must read the contents of `metadata.json` directly from the compressed stream into your script's memory/variables.
3. **Validation**: Parse the streamed `metadata.json`. Only accept the artifact if the `"type"` field is exactly `"binary"` and the `"status"` field is `"release"`.
4. **Path Manipulation (Content-Addressable Storage)**: For valid artifacts, calculate the SHA-256 checksum of the *archive file itself*. Copy the archive into the repository using a sharded path structure based on the hash: 
   `/home/user/repo/artifacts/<first-2-characters-of-hash>/<full-hash>.<original-extension>`
5. **Atomic Manifest Updates**: The repository maintains a global manifest at `/home/user/repo/manifest.json` (which begins as an empty JSON array `[]`). For each valid artifact, augment its parsed `metadata.json` object with a new key `"sha256"` containing the file's hash. Append this augmented JSON object to the JSON array in `manifest.json`. 
   **Crucial**: The manifest update must be atomic. You must write the updated JSON array to a temporary file in `/home/user/repo/` and use a single atomic operation (e.g., `mv`) to replace the active `manifest.json`. This ensures the manifest is never left in a corrupted state if the script is interrupted.

Initialize the repository by creating `/home/user/repo/artifacts/` and a valid empty JSON array in `/home/user/repo/manifest.json`. Then, run your `/home/user/curator.sh` script to process the incoming directory. 

Leave the final, correctly curated repository in `/home/user/repo/` for automated verification.