You are an artifact manager responsible for curating large binary repositories. Upstream systems frequently drop large, compressed archives into an incoming queue. Your task is to build a Go-based daemon that automatically processes these incoming artifacts, chunks large files to meet storage backend constraints, and repackages them.

Specifically, you need to write a Go program at `/home/user/artifact_manager/main.go` that does the following:

1. **Watch a directory:** Continuously monitor `/home/user/incoming` for new `.tar.gz` files. You can use polling (e.g., checking every 1 second) or `github.com/fsnotify/fsnotify`.
2. **Stream-process and Extract:** When a `.tar.gz` file arrives (e.g., `release.tar.gz`), extract its contents to a temporary directory.
3. **Chunking:** Scan the extracted files. If any file is strictly greater than 1,024,000 bytes (1000 KB), split it into smaller files of exactly 1,024,000 bytes (the final chunk may be smaller). Name the chunks by appending `.part0`, `.part1`, etc., to the original filename. Remove the original extracted large file after chunking. Files 1,024,000 bytes or smaller should remain untouched.
4. **Repackage:** Compress the resulting files (chunks and untouched small files) into a new `.zip` archive. Place this zip file in `/home/user/outgoing/` with the same base name as the original (e.g., `release.zip`).
5. **Logging:** Append an entry to `/home/user/artifact_log.jsonl` (JSON Lines format) for every processed archive. The JSON object must have this exact structure:
   ```json
   {
     "original_archive": "release.tar.gz",
     "repackaged_archive": "release.zip",
     "chunked_files": {
       "large_binary.bin": 3
     }
   }
   ```
   (Where the `chunked_files` map contains the original filename as the key and the total number of chunks it was split into as the value. Do not include files that were not chunked in this map).

**To complete the task:**
1. Initialize a Go module in `/home/user/artifact_manager`.
2. Write and compile your Go program.
3. Start your program in the background.
4. Run the pre-existing script `/home/user/generate_test_data.sh`. This script will create a file at `/tmp/payload.tar.gz`.
5. Move `/tmp/payload.tar.gz` into `/home/user/incoming/` to trigger your daemon.
6. Wait for your daemon to process the file, producing `/home/user/outgoing/payload.zip` and appending to `/home/user/artifact_log.jsonl`.
7. Exit once the processing is verifiable.