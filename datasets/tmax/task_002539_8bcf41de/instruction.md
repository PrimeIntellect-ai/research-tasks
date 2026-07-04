You are tasked with organizing a massive dump of raw data files for our project, generating a verified manifest, and exposing the organized files via our custom vendored Bash HTTP server.

**Stage 1: Parsing and Bulk Renaming**
We have a directory containing raw data dumps at `/app/raw_data/`. There are numerous files named `dump_<id>.dat`. 
Each file is a text file where the first line is exactly `CATEGORY: <category_name>` and the second line is `TIMESTAMP: <epoch_time>`. 
You must:
1. Stream read the files to extract the category and timestamp.
2. Bulk move and rename these files to `/app/organized_data/<category_name>/<epoch_time>.log`.
3. To speed this up, you must process files concurrently (e.g., using background jobs or `xargs -P`).
4. Whenever a file is successfully moved, append a line to `/app/organized_data/processed.log` in the format: `MOVED dump_<id>.dat TO <category_name>/<epoch_time>.log`. 
   *CRITICAL:* Because you are processing concurrently, you MUST use `flock` when appending to `/app/organized_data/processed.log` to prevent race conditions and interleaved writes.

**Stage 2: Manifest Generation**
Once all files are organized, generate a SHA256 checksum manifest of all the `.log` files in `/app/organized_data/` (excluding `processed.log`). 
Save this manifest exactly at `/app/organized_data/manifest.sha256`. The format should be standard `sha256sum` output (e.g., `<hash>  category/timestamp.log`). Run the checksums using relative paths from within the `/app/organized_data/` directory.

**Stage 3: Vendored Package Patching**
We use a lightweight, vendored bash HTTP server to serve these files to other microservices. Its source code is located at `/app/bash-serve-v1.2/serve.sh`. 
However, it currently has two bugs:
1. It ignores the `BASE_DIR` environment variable and defaults to `/tmp/www`. You need to fix it so it serves files from the directory specified in `BASE_DIR`.
2. The authentication check is broken. It expects an `Authorization: Bearer <token>` header, but it currently only checks if the header contains the word "Bearer", rather than validating the actual token against the `AUTH_TOKEN` environment variable. Fix the script to strictly require the exact token.

**Stage 4: Start the Server**
Run the patched server in the background, listening on `127.0.0.1:9090`.
- Export `BASE_DIR=/app/organized_data`
- Export `AUTH_TOKEN=secret-token-88`
- Start the server: `/app/bash-serve-v1.2/serve.sh 9090 &`

Leave the server running. Our automated systems will test your organization by querying the manifest and data files over HTTP with the provided token.