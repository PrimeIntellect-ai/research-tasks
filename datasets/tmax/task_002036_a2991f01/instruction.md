You are helping a developer organize and migrate a chaotic directory of legacy data files into a newly architected storage system. Additionally, you need to establish a basic CI/CD pipeline script and performance benchmark for the migration tool.

You must write a Python script and a Bash script to fulfill the requirements below.

**Context & Requirements:**
1. **Input Data**: You will find legacy data files in the directory `/home/user/legacy_data/`. The files are in JSON Lines format (`.jsonl`). Each line represents a record with the old schema: 
   `{"id": <int>, "data": "<string>", "crc32": "<hex_string>"}`

2. **Data Integrity (Checksums)**: Over time, some records suffered bit-rot. The `crc32` field contains the expected CRC32 checksum (as a hexadecimal string, e.g., "a1b2c3d4") of the `data` string. 
   - Your script must compute the CRC32 checksum of the `data` string (use Python's `zlib.crc32`).
   - If the computed checksum does NOT match the provided `crc32` hex string, the record is corrupt and MUST be dropped.

3. **Schema Migration & Organization**: 
   - For every valid record, generate a `record_id` which is the SHA-256 hash (hexadecimal) of the `data` string.
   - The new schema should be: `{"record_id": "<sha256_hex>", "content": "<data>"}`
   - Save each valid record as a separate JSON file organized into a sharded directory structure:
     `/home/user/new_data/<first_2_characters_of_sha256>/<sha256_hex>.json`
   - Example: If the SHA-256 hash is `e3b0c442...`, the file should be saved at `/home/user/new_data/e3/e3b0c442....json`.

4. **Benchmarking**:
   - The Python script must be named `/home/user/migrate.py`.
   - It must measure the wall-clock time taken to process all files and perform the I/O.
   - Upon completion, the script must output a benchmark report to `/home/user/benchmark_report.json` containing exactly this structure:
     `{"total_valid": <int>, "total_invalid": <int>, "records_per_second": <float>}`

5. **CI/CD Pipeline Setup**:
   - Create a bash script at `/home/user/ci_pipeline.sh`. Make sure it is executable.
   - The script should run `/home/user/migrate.py`.
   - After the Python script finishes, the bash script must read `/home/user/benchmark_report.json`.
   - If the `total_invalid` count is greater than or equal to `total_valid`, the pipeline should fail (exit code 1).
   - Otherwise, it should print `CI SUCCESS` to standard output and succeed (exit code 0).

Start by inspecting the `/home/user/legacy_data/` directory, then write and test the necessary scripts.