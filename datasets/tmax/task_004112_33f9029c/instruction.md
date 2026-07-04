You are a storage administrator responding to a security incident. A rogue process has encrypted a system archive and attempted to inject malicious files using a directory traversal ("zip slip") attack. 

Your task consists of four phases:

**Phase 1: Key Recovery from Video**
You have been provided with a surveillance video of the compromised server's status LED at `/app/incident.mp4`. The LED flashes encode the XOR encryption key used by the rogue process.
1. Extract the frames of the video (using `ffmpeg`).
2. Calculate the average grayscale brightness of each frame. 
3. Treat frames with an average brightness > 100 as `1`, and <= 100 as `0`.
4. Group the bits into 8-bit bytes (Big-Endian) to recover the ASCII key string.

**Phase 2: Archive Decryption and Parsing**
An encrypted archive is located at `/home/user/corrupt_backup.wal`. 
Write a C program that:
1. XOR-decrypts the file using the key recovered in Phase 1 (repeating the key cyclically).
2. Parses the decrypted data. The custom `.wal` format consists of sequential entries:
   - `Path Length` (2-byte unsigned integer, little-endian)
   - `Path` (ASCII string of length `Path Length`)
   - `Data Length` (4-byte unsigned integer, little-endian)
   - `Data` (Raw bytes of length `Data Length`)

**Phase 3: Zip-Slip Mitigation**
As your C program parses the archive, it must extract the files to `/home/user/recovered_files/`.
*CRITICAL:* You must mitigate "zip-slip" attacks. If a parsed `Path` contains the substring `../` anywhere, or starts with `/`, it is malicious. **Do not extract these files.** Only extract safe paths (relative paths without parent directory traversal).

**Phase 4: Storage Optimization**
To save disk space, find all duplicate files within `/home/user/recovered_files/` (files with identical binary content) and replace the duplicates with hard links to the original. You may use shell built-ins, `sed`, `awk`, and standard CLI tools to accomplish this step.

Complete these steps and leave the correctly extracted, deduplicated files in `/home/user/recovered_files/`.