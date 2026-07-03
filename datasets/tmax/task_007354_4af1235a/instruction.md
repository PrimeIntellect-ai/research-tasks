You are an AI assistant acting as an automated artifact manager curating a local binary repository. 

Your system has received a batch of legacy artifact uploads. The upload log is encoded in ISO-8859-1 (Latin-1) and contains multi-line records. Some uploads failed, and some succeeded. 
Your task is to parse this log, extract the successfully uploaded nested archives, and build an inventory file safely using concurrent processes.

Here are your instructions:

1. **Setup Workspace:**
   All operations should occur in `/home/user/artifact_manager/`. The log file is located at `/home/user/artifact_manager/uploads.log`. 
   The binary artifacts are located in `/home/user/artifact_manager/binaries/`.

2. **Log Parsing & Encoding:**
   The `uploads.log` is encoded in ISO-8859-1. Each upload record spans exactly 4 lines, formatted like this:
   ```
   START_RECORD
   File: /home/user/artifact_manager/binaries/bundle_1.tar.gz
   Status: SUCCESS (or FAILED)
   END_RECORD
   ```
   You must first convert this log to UTF-8. Then, extract the file paths of only the artifacts with a `SUCCESS` status.

3. **Archive Extraction & File Locking (Rust):**
   Write a Rust project in `/home/user/artifact_manager/curator/` that takes a single file path as a command-line argument.
   For each provided path, the Rust program must:
   - Extract the `.tar.gz` file to a temporary location. Inside each `.tar.gz` is exactly one `.zip` file.
   - Extract that inner `.zip` file into `/home/user/artifact_manager/curated/`.
   - After extracting the inner zip, the program must securely append the names of the final extracted files to `/home/user/artifact_manager/inventory.txt`. 
   - **Crucial:** Because this Rust program will be called concurrently, it **must** use file-system level locking (e.g., using `fs4` or `fd-lock` crate) when writing to `inventory.txt` to prevent data corruption. 
   The format for the inventory file should be: `[<OuterArchiveName>] <ExtractedFileName>`.

4. **Concurrent Execution:**
   Write a bash script at `/home/user/artifact_manager/run_all.sh` that takes the successfully parsed file paths from step 2, builds your Rust tool, and invokes the Rust tool for each file **concurrently** (e.g., using `xargs -P 4` or background bash jobs).

5. **Final Output:**
   Run your bash script. Once complete, sort the resulting `/home/user/artifact_manager/inventory.txt` alphabetically and save it to `/home/user/artifact_manager/final_inventory.txt`.