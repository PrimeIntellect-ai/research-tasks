You are acting as an artifact manager for a binary repository. We are migrating our raw artifact storage to a new curated format.

Your task is to write and execute a Python script (`/home/user/curate.py`) that processes a set of raw compressed artifacts and reorganizes them into a curated directory.

**Source Directory:** `/home/user/artifacts_raw/` (contains nested directories with `.tar.gz` files).
**Target Directory:** `/home/user/artifacts_curated/` (you must create this directory if it doesn't exist).

**Processing Requirements:**
1. **Traverse:** Recursively search `/home/user/artifacts_raw/` for all `.tar.gz` files.
2. **Stream Processing & Config Interpretation:** Without extracting the entire archive to disk, read the contents of `meta.ini` located at the root of each `.tar.gz` file. 
   - `meta.ini` contains an `[Artifact]` section with two keys: `id` (a unique string) and `payload_file` (the name of the binary file inside the archive).
3. **Format Conversion:** Convert the parsed `meta.ini` data into a JSON file at `/home/user/artifacts_curated/<id>.json`. The JSON must be a single object containing the keys `id` and `payload_file` with their respective values.
4. **Binary Processing:** Read the binary file specified by `payload_file` from the archive. Prepend the exact 8-byte ASCII string `CURATED_` to this binary data.
5. **Output:** Write the modified binary data to `/home/user/artifacts_curated/<id>.bin`.

**Example `meta.ini`:**
```ini
[Artifact]
id=alpha_99
payload_file=blob.dat
```
For the above example, you would create `/home/user/artifacts_curated/alpha_99.json` and `/home/user/artifacts_curated/alpha_99.bin`.

Ensure your Python script processes all `.tar.gz` files found in the source directory and handles the binary operations correctly. Run your script to complete the curation.