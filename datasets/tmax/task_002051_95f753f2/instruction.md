You are tasked with resolving a critical storage management issue caused by a failing backup system. A legacy backup script has been following symlinks into infinite loops, consuming massive amounts of disk space and generating corrupted manifests.

Your objective has two parts:

**Part 1: Video Forensic Analysis**
We have a screen recording of the console when the backup system crashed, located at `/app/backup_dash.mp4`. 
1. Use tools like `ffmpeg` and `tesseract-ocr` (which you can install if needed) to analyze the video.
2. Find the exact path where the disk space was exhausted. The video shows a console error message in the format: `FATAL: Disk space exhausted in /var/backups/XYZ_ARCHIVE_NAME`.
3. Create an empty directory in `/home/user/` named exactly matching the `XYZ_ARCHIVE_NAME` found in the video.

**Part 2: Robust Manifest Parser (Bash)**
You must write a robust Bash script at `/home/user/safe_manifest_parser.sh` that can parse our proprietary backup manifest format, resolve symlinks, and safely detect infinite loops.

The script must read from `stdin`. The input will be a stream of pipe-separated values representing the file system state.
Each line has the format: `FILEPATH|TYPE|TARGET_OR_HASH`
- `FILEPATH`: The absolute path of the item (e.g., `/var/data/file1`).
- `TYPE`: Either `F` (File) or `S` (Symlink).
- `TARGET_OR_HASH`: If `TYPE` is `F`, this is a SHA-256 checksum. If `TYPE` is `S`, this is the absolute path to another item.

Your script must process this input and output a resolved manifest to `stdout`.
For every item (both `F` and `S`) in the input, you must trace it to its final target:
1. If an item ultimately resolves to a File (`F`), output: `FILEPATH|RESOLVED|SHA_256_HASH`
2. If an item resolves to a path that does not exist in the manifest, or if following the symlinks results in an infinite loop, output: `FILEPATH|BROKEN`

Rules for the Bash script:
- The output must be sorted lexicographically by `FILEPATH`.
- You must use pure Bash or standard coreutils (`awk`, `grep`, `sort`, etc.). 
- The script must correctly handle infinite cyclic symlink loops (e.g., A -> B, B -> C, C -> A) without hanging or crashing.
- Your script will be tested against thousands of randomized manifests to ensure it behaves exactly like our reference implementation.

Please complete the video analysis to create the required directory, and write the `/home/user/safe_manifest_parser.sh` script.