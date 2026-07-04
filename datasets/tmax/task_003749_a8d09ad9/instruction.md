You are an AI assistant helping a climate researcher fix their automated dataset ingestion pipeline and write a dataset organization tool. 

The task consists of two parts:

### Part 1: Fix the Ingestion Pipeline
The researcher has a local multi-service ingestion pipeline located in `/app/ingestion/`. It consists of four components:
1. **Nginx** (Reverse proxy, listens on port 8080)
2. **Flask API** (Receives file uploads)
3. **Redis** (Message broker)
4. **Python Worker** (Processes uploaded archives)

Currently, the pipeline is broken. The Nginx configuration `/app/ingestion/nginx.conf` is forwarding traffic to the wrong internal port for the Flask API, and the worker configuration `/app/ingestion/worker.env` is pointing to the wrong Redis port. 
- You need to inspect the pipeline, correct the configuration files so Nginx points to the Flask API socket/port, and the worker connects to the correct Redis instance.
- Once fixed, use `/app/ingestion/start_services.sh` to start the pipeline.
- Verify the end-to-end flow works by running: `curl -F "file=@/app/sample_dataset.tar.gz" http://127.0.0.1:8080/upload`. If successful, the worker will extract it into `/home/user/staging/<job_id>/`.

### Part 2: Write the Dataset Linker
The worker extracts nested archives and creates a multi-line log file named `manifest.txt` in the staging directory. 

You must write a Bash script at `/home/user/dataset_linker.sh` that takes two arguments:
`./dataset_linker.sh <source_staging_dir> <target_organized_dir>`

The script must perform the following:
1. Read the `manifest.txt` located in `<source_staging_dir>`. The manifest contains multi-line records separated by `---`:
   ```
   Filename: <filename.ext>
   Category: <category_name>
   SHA256: <expected_hash>
   ---
   ```
2. For each record, find the file named `<filename.ext>` somewhere within the `<source_staging_dir>` (it could be deeply nested).
3. Compute the SHA256 checksum of the found file and verify it matches the `<expected_hash>` from the multi-line record.
4. If the checksum matches, create a hard link to this file in `<target_organized_dir>/<category_name>/<filename.ext>`. 
5. If the checksum does not match, or the file is missing, skip it.
6. Make sure to create the category subdirectories inside `<target_organized_dir>` if they do not exist.

Your script must be robust. The automated verification system will test your `dataset_linker.sh` against thousands of procedurally generated staging directories to ensure exact bit-for-bit equivalence in the generated directory structure compared to a reference implementation.

Make sure your script is executable (`chmod +x /home/user/dataset_linker.sh`).