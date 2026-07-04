You are a backup administrator responsible for securely archiving updated system files. 

Your objective is to perform a custom differential backup of the directory `/home/user/data/` based on a previous state, compress and chunk the archive, and ensure the chunks are written to the disk atomically.

Here are the specific requirements:
1. **Differential Selection**: Look at the manifest file `/home/user/baseline.txt`. It contains the state of the previous backup in the format `<SHA256-hash>  <filename>`. Compare the current files in `/home/user/data/` against this baseline. Identify all files that are newly added or have a different SHA256 hash.
2. **Archiving & Compression**: Create a single `tar` archive containing ONLY the new and modified files (preserve their relative paths from within `/home/user/data/`). Compress this archive using standard `gzip`.
3. **Chunking & Atomic Writing**: 
   - Split the compressed gzip file into chunks of exactly 50 KB (51200 bytes).
   - Write these chunks to the directory `/home/user/backup_out/`.
   - **Crucial**: You must use atomic file writes. Write each chunk to a temporary file named `part-XXX.tmp` (where XXX is a zero-padded 3-digit number starting at 000). Once the chunk is completely written to the disk, rename it to `part-XXX.bck`.
   - Log every successful rename operation to `/home/user/atomic_ops.log` in the exact format: `Renamed part-XXX.tmp to part-XXX.bck`.
4. **New Baseline**: Finally, calculate the SHA256 hashes of all current files in `/home/user/data/` and write them to `/home/user/new_baseline.txt` (using the same `<hash>  <filename>` format). This file must also be written atomically (written to `/home/user/new_baseline.tmp` first, then renamed).

Complete the task using any combination of shell commands or a custom script in the language of your choice. Ensure `/home/user/backup_out/` is created if it does not exist.