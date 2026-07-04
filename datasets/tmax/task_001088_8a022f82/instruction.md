You are tasked with building a secure configuration chunk filter in C for a configuration manager. The system receives configuration updates as gzipped custom binary files, but some of these updates have been corrupted or deliberately tampered with by a malicious actor trying to drop database tables. 

Additionally, the exact version number required for valid configurations is dynamically tied to a visual changelog video recorded during the config session.

**Step 1: Video Analysis**
There is a video file located at `/app/config_session.mp4`. To find the valid configuration version number (`K`), you must analyze this video and count the exact number of **I-frames (keyframes)** it contains. You can use `ffmpeg` or `ffprobe`, which are pre-installed. The integer count of I-frames is the required version number `K`.

**Step 2: The Configuration Filter (C Program)**
Write a C program at `/home/user/config_filter.c` and compile it to `/home/user/config_filter`. It must link against `zlib` (`-lz`). 
The program must accept a single command-line argument: the path to a gzipped configuration chunk file.

The program must:
1. Open and decompress the gzipped file stream on the fly.
2. Parse the custom binary header (uncompressed format):
   - Bytes 0-3: Magic number. Must be exactly `CFG!` (ASCII).
   - Bytes 4-5: Version number (unsigned 16-bit integer, little-endian). Must exactly match the I-frame count `K` from Step 1.
   - Bytes 6-7: Encoding flag (unsigned 16-bit integer, little-endian). `0` means ASCII, `1` means UTF-16LE.
3. Read the rest of the uncompressed data as the payload.
4. If the encoding is UTF-16LE, convert the payload to ASCII (you may assume characters are within the standard ASCII range, simply padded with null bytes).
5. Check the resulting ASCII payload for the exact substring `DROP_TABLE`.

**Validation Rules:**
Your program must exit with status code `0` (Clean/Accept) ONLY IF:
- The magic number is correct.
- The version matches `K`.
- The payload does NOT contain the substring `DROP_TABLE`.

If ANY of these conditions fail (wrong magic, wrong version, or malicious substring found), the program must exit with status code `1` (Evil/Reject). If the file cannot be opened or is invalid gzip, exit with `1`.

**Step 3: Verification Corpus**
There are two directories containing test files:
- `/app/corpus/clean/`
- `/app/corpus/evil/`

Your compiled binary `/home/user/config_filter` will be tested against every file in both directories. It must preserve/accept (exit `0`) 100% of the clean files, and reject (exit `1`) 100% of the evil files.