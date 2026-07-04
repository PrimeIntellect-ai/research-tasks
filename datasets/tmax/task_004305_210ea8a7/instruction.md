You are a developer tasked with organizing and restoring project files from a proprietary incremental backup system. We have inherited some backup archives in a custom format (`.cba` - Custom Backup Archive), but the original extraction tool is lost, and we suspect some of these archives were tampered with to include path traversal (zip-slip) attacks.

Your task is to write a Go program (`/home/user/extractor.go`) that parses these binary archives, applies the incremental updates sequentially, safely extracts the files to a target directory, and verifies the final state.

The `.cba` file format is as follows:
1. **Magic Header:** The first 4 bytes are exactly `CBA1`.
2. **Records:** Followed by a sequence of file records until EOF. Each record consists of:
   - **Path Length:** 2 bytes, unsigned integer, Little Endian.
   - **Path:** UTF-8 string of length specified above. (Paths are relative to the project root).
   - **Operation:** 1 byte. `0x00` means Add/Modify. `0x01` means Delete.
   - **Compressed Size:** 4 bytes, unsigned integer, Little Endian. (Present ONLY if Operation is `0x00`).
   - **File Data:** Zlib-compressed file data of length `Compressed Size`. (Present ONLY if Operation is `0x00`).

Requirements for your Go tool:
1. **Input/Output:** Your tool should accept a target output directory and a list of `.cba` files in chronological order. Example: `go run extractor.go -out /home/user/project_workspace base.cba inc1.cba inc2.cba`
2. **Incremental Logic:** 
   - Apply the files in the order provided.
   - If a file is Add/Modify (`0x00`), decompress and write/overwrite it in the target directory.
   - If a file is Delete (`0x01`), remove it from the target directory if it exists.
3. **Zip-Slip Prevention:** As you extract paths, if any path attempts to traverse outside the target directory (e.g., contains `../` segments that escape the root, or is an absolute path), **do not extract it**. Instead, append the exact malicious path string found in the archive to `/home/user/malicious_paths.log` (one path per line).
4. **Manifest Generation:** After applying all archives, recursively traverse the output directory and create a manifest file at `/home/user/manifest.txt`. Each line should contain the relative path (from the output directory) and the SHA-256 hash of the file, separated by two spaces: `[relative/path]  [sha256_hex]`. Sort the manifest lines alphabetically by path.

Setup:
The archives are located at `/home/user/backups/`:
- `/home/user/backups/base.cba`
- `/home/user/backups/inc1.cba`
- `/home/user/backups/inc2.cba`

Extract these archives sequentially into the empty directory `/home/user/project_workspace`.

Make sure you run your tool and verify that `/home/user/project_workspace`, `/home/user/manifest.txt`, and `/home/user/malicious_paths.log` are correctly populated.