You are an artifact manager responsible for curating a binary repository. You have been given a set of raw binary artifacts and their corresponding multi-line build logs. Your task is to write a Python script that processes these logs, identifies successfully built artifacts, calculates their cryptographic hashes using memory-efficient streaming, and packages them into a final curated archive.

Here are the details of your environment and requirements:

1. **Inputs:**
   - **Logs Directory:** `/home/user/artifacts/logs/` contains `.log` files.
   - **Binaries Directory:** `/home/user/artifacts/raw/` contains `.bin` files.

2. **Log Format:**
   The logs contain multi-line build records. Each record starts with `=== BUILD RECORD START ===` and ends with `=== BUILD RECORD END ===`.
   Within a record, you will find:
   - `Artifact: <filename>` (e.g., `Artifact: app-1.0.bin`)
   - A multi-line trace of build steps.
   - `Result: <STATUS>` (where `<STATUS>` is either `SUCCESS` or `FAILED`)
   
   *Note: A single log file may contain multiple build records. You must parse these multi-line blocks to determine which artifacts succeeded.*

3. **Processing Requirements:**
   Write a Python script at `/home/user/curate.py` that performs the following operations:
   - **Parse Logs:** Read through all `.log` files in the logs directory. Identify all artifacts that have a `Result: SUCCESS`. Ignore `FAILED` artifacts.
   - **Streaming Hash Calculation:** For each successful artifact found in the raw binaries directory, calculate its SHA256 hash. You **must** read the binary files in chunks (e.g., 64KB chunks) or use `mmap` to avoid loading entire binaries into memory at once, as the real system handles multi-gigabyte files.
   - **Manifest Generation:** Create a JSON file at `/home/user/manifest.json` mapping the successful artifact filenames to their SHA256 hashes.
     Format example:
     ```json
     {
       "app-1.0.bin": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
     }
     ```
   - **Archive Creation:** Create an uncompressed tar archive at `/home/user/curated_repo.tar` containing ONLY the successful `.bin` files. The files in the tarball should not include the parent directory structure (i.e., when extracted, `app-1.0.bin` should be in the current directory, not inside `artifacts/raw/`).

4. **Execution:**
   Once you have written the script, execute it to generate `/home/user/manifest.json` and `/home/user/curated_repo.tar`.