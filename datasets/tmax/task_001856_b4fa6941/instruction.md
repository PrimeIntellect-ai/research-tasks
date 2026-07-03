You are a backup administrator tasked with archiving and deduplicating backup blocks based on their binary headers.

You have a directory of raw backup files located at `/home/user/raw_backups/`. 
Each file has a `.dat` extension. To optimize storage and indexing, you need to write a Go program (`/home/user/processor.go`) that performs the following steps:

1. Creates an output directory `/home/user/processed_backups/`.
2. Iterates over all `.dat` files in `/home/user/raw_backups/` in alphabetical order.
3. For each file, extracts exactly the first 16 bytes. This 16-byte sequence is the "backup block header".
4. Computes the SHA-256 checksum (in lowercase hex) of this 16-byte header.
5. Copies the files into `/home/user/processed_backups/` with the following rule:
   - If this is the *first* time you are seeing this specific 16-byte header, copy the file to `/home/user/processed_backups/` keeping its original filename.
   - If you have seen this 16-byte header before in an earlier file (alphabetically), do *not* copy the file contents. Instead, create a **hard link** in `/home/user/processed_backups/` with the current filename that points to the *first* file copied that had this same header.
6. Generates a manifest file mapping each original filename to the SHA-256 hash of its 16-byte header. 
   - The format for each line must be: `<filename> <sha256_hex>` (e.g., `file_A.dat a1b2c3...`).
   - The manifest must be sorted alphabetically by filename.
   - To prevent corruption during generation, write the manifest data to a temporary file in `/home/user/processed_backups/` first, and then use an atomic write (rename) to move it to `/home/user/processed_backups/manifest.txt`.

Write and execute the Go program so that the final state is achieved.