You are tasked with building a robust, concurrent artifact ingestion script for a binary repository. As an artifact manager, you need to securely process large binary files, chunk them, archive them, and ensure that concurrent writes do not corrupt the repository.

Please write a Bash script at `/home/user/artifact_ingest.sh` that fulfills the following requirements:

1. **Input**: The script must accept exactly one argument: the absolute path to a file to be ingested.
2. **Hashing**: Compute the SHA256 checksum of the original input file.
3. **Concurrency Control**: Before writing anything to the repository directory (`/home/user/repo/`), the script must acquire an exclusive file lock on `/home/user/repo/repo.lock` using the `flock` command to prevent race conditions from concurrent ingestions.
4. **Storage Creation**: Create a directory for the artifact at `/home/user/repo/<original_file_sha256>/`.
5. **Archiving, Compression, and Splitting**: 
   - Archive the input file using `tar`. (Ensure the tarball only contains the file's basename, not the full absolute path. Use `tar -C` appropriately).
   - Pipe the tar output through `gzip` for compression.
   - Pipe the compressed stream into `split` to divide it into chunks of exactly 1 Megabyte (`1M`).
   - The chunks should be saved directly into the newly created artifact directory with the prefix `chunk_`. (e.g., `chunk_aa`, `chunk_ab`).
6. **Manifest Generation**: Inside the artifact directory, generate a `manifest.txt` file exactly matching this format:
   ```
   Original: <basename_of_input_file>
   Original-SHA256: <original_file_sha256>
   Chunks:
   chunk_aa <sha256_of_chunk_aa>
   chunk_ab <sha256_of_chunk_ab>
   ```
   (List all chunks in alphabetical order, followed by a space and their respective SHA256 checksums).
7. **Lock Release**: Release the `flock` after the manifest is completely written.

Once your script is written and made executable (`chmod +x /home/user/artifact_ingest.sh`), there are 5 binary files located in `/home/user/incoming/` (named `file1.bin` to `file5.bin`). 

You must execute your script concurrently on all 5 files in `/home/user/incoming/` using a tool like `xargs -P 5` or `parallel` to demonstrate that your locking mechanism works.

**Environment details:**
- Incoming directory: `/home/user/incoming/`
- Repository directory: `/home/user/repo/`
- Script path: `/home/user/artifact_ingest.sh`