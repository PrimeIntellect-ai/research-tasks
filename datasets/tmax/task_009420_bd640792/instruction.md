You are an artifact manager responsible for curating our local binary repository. Recently, a poorly written backup script followed symlinks into an infinite loop, generating a massive, corrupted multi-line manifest file. It recorded the same artifacts multiple times under increasingly deep paths, and sometimes split the records.

Your task is to write a Rust utility that parses this corrupted log, deduplicates the entries, verifies the actual files, and generates a clean, authoritative JSON manifest. 

Here are the details:

1. **Environment:**
   - Raw log file: `/home/user/corrupt_manifest.log`
   - Artifacts directory: `/home/user/artifacts/`

2. **Log Format:**
   The log consists of multi-line records separated by a line containing exactly `---`. 
   Example:
   ```
   [Artifact]
   ID: 1042
   Path: /home/user/artifacts/loop/link/link/link/alpha.bin
   Status: verified
   ---
   ```

3. **Requirements for your Rust program:**
   - Create a new Rust project at `/home/user/artifact_parser`.
   - Parse the multi-line records from `/home/user/corrupt_manifest.log`.
   - For each record, extract the `ID`, `Path`, and `Status`.
   - **Canonicalization & Deduplication:** Many paths point to the same file due to symlink loops (e.g., `loop/link/link.../file`). You must resolve the absolute, canonical path of the file. If multiple records resolve to the *same* canonical file, keep only the record with the *highest* `ID`. Ignore records where the `Status` is not `verified`, or where the file does not actually exist on disk.
   - **Checksum Generation:** For each uniquely resolved, valid artifact, compute its SHA-256 checksum.
   - **Output:** Write the final curated list to `/home/user/final_manifest.json` as a JSON array of objects, sorted in ascending order by `ID`.

4. **Expected Output Format (`/home/user/final_manifest.json`):**
   ```json
   [
     {
       "id": 1042,
       "canonical_path": "/home/user/artifacts/loop/alpha.bin",
       "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
     }
   ]
   ```

Use only standard Linux tools and Rust (you may use crates like `serde`, `serde_json`, `sha2`, and `hex` by adding them to your `Cargo.toml`). Compile and run your Rust program to generate the final JSON manifest.