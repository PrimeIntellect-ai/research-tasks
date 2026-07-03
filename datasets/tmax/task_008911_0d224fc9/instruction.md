You are acting as an artifact manager for a software company. During a recent data migration, a backup of our binary artifact repository was heavily fragmented. The large binary artifacts were split into chunks, and the chunk files were given scrambled, meaningless names. 

Fortunately, we have a manifest file that maps the original artifacts to their scrambled chunks. Your task is to reconstruct the artifacts, verify their integrity, and organize them into a curated repository.

Here are the details:
1. **Manifest File**: Located at `/home/user/manifest.json`. This JSON file contains a list of objects under the key `"artifacts"`. Each object has:
   - `canonical_name`: The original name of the artifact (e.g., `firmware_v2.1.bin`).
   - `chunks`: A list of scrambled chunk filenames in the exact order they must be merged.
   - `expected_sha256`: The SHA256 checksum of the fully reconstructed (merged) binary artifact.

2. **Raw Chunks Directory**: All the scrambled chunk files are located in `/home/user/raw_chunks/`. These are binary files.

3. **Output Directory**: You must create a directory at `/home/user/curated_artifacts/`.

**Your Instructions**:
Write and execute a Python script to do the following:
- Parse `/home/user/manifest.json`.
- For each artifact, read its corresponding binary chunks from `/home/user/raw_chunks/` and merge them in the specified order.
- Calculate the SHA256 checksum of the merged binary data.
- **Integrity Verification**: 
  - If the calculated SHA256 matches the `expected_sha256`, save the merged binary into `/home/user/curated_artifacts/` using its `canonical_name`.
  - If the calculated SHA256 does **not** match (indicating corruption), DO NOT save the binary. Instead, append the `canonical_name` to a log file located at `/home/user/curated_artifacts/integrity_failures.log` (one name per line).

Ensure that your script handles the binary I/O correctly and completely processes the manifest.