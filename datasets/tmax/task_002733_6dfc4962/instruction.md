You are an AI assistant helping a geophysics researcher organize and process a batch of raw sensor datasets. 

The researcher has downloaded several dataset archives into the `/home/user/datasets/` directory. Due to an unstable connection, some of these `.zip` archives are corrupted. Each valid archive contains a single large binary file named `measurements.bin`. 

The researcher needs you to write and execute a Python script that does the following:
1. **Archive Verification:** Iterate through all `.zip` files in `/home/user/datasets/` and verify their integrity. Ignore any corrupted archives.
2. **Temporary Management:** For each valid archive, securely extract `measurements.bin` into a temporary directory using Python's `tempfile` module. Ensure temporary files are cleaned up after processing each archive.
3. **Memory-Mapped Search:** The `measurements.bin` files are theoretically too large to load entirely into RAM. Use Python's `mmap` module to efficiently scan the extracted binary file for the exact byte signature `b'ANOMALY_778'`.
4. **Atomic Write:** Collect the starting byte offsets of every occurrence of this signature for each valid archive. Save this data as a JSON object where the keys are the valid zip filenames (e.g., `"data_01.zip"`) and the values are lists of integers representing the byte offsets (e.g., `[1024, 4096]`). Write this JSON dictionary *atomically* to `/home/user/anomaly_report.json` (i.e., write to a temporary file first, then safely replace/rename it to the final destination to prevent partial reads by other monitoring processes).

**Formatting constraints for the final output:**
- The final file must be located at `/home/user/anomaly_report.json`.
- It must be a valid JSON file.
- Example format:
```json
{
  "dataset_A.zip": [150, 89340],
  "dataset_B.zip": []
}
```

Write the script, execute it, and ensure the `anomaly_report.json` file is successfully created with the correct data.