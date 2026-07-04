Hello! I'm a researcher organizing a massive collection of compressed datasets submitted by third parties. Unfortunately, some of these archives are poorly formatted or maliciously constructed (e.g., containing infinite symlink loops, zip bombs, or absolute paths that could overwrite system files). 

I need you to build a robust Python filter to sanitize these dataset archives. 

Here is the multi-stage workflow you need to complete:

**1. Extract Configuration from Video**
I recorded a script execution that visually outputs our system constraints as flashes of color in a video located at `/app/system_limits.mp4`. 
- You need to extract the frames from this video.
- Count the exact number of purely Red frames (RGB: 255, 0, 0) to determine the `MAX_SYMLINK_DEPTH`.
- Count the exact number of purely Blue frames (RGB: 0, 0, 255) to determine the `MAX_FILES_PER_ARCHIVE`.
*(Note: A frame is considered purely red or blue if the center pixel of the frame matches the exact RGB value. The background is black).*

**2. Generate Configuration File**
I have a template configuration file at `/home/user/config_template.json`. It looks like this:
```json
{
  "max_depth": PLACEHOLDER_DEPTH,
  "max_files": PLACEHOLDER_FILES
}
```
Use shell tools (like `sed` or `awk`) to replace `PLACEHOLDER_DEPTH` and `PLACEHOLDER_FILES` with the counts you found in the video, and save the result to `/home/user/config.json`.

**3. Build the Archive Filter**
Write a Python script at `/home/user/dataset_filter.py` that takes a single command-line argument (the path to an archive) and determines if it is safe.
The script must:
- Read limits from `/home/user/config.json`.
- Support both `.zip` and `.tar.gz` archives.
- **DO NOT** extract the files to disk. You must inspect the metadata/headers inside the compressed streams.
- **Reject** the archive (exit code 1) if:
  - It contains more files than `max_files`.
  - It contains any file paths that are absolute (e.g., starting with `/`).
  - It contains any file paths that attempt path traversal (e.g., containing `../`).
  - It contains symlinks that point outside the archive root or form a chain longer than `max_depth`. (You must simulate resolving the symlinks internally based on the archive's metadata to detect loops or depth violations).
- **Accept** the archive (exit code 0) if it passes all checks.

**4. Validation**
I have provided two directories of test archives:
- `/app/corpora/clean/`: Contains valid, safe datasets. Your script MUST exit with 0 for all files in this directory.
- `/app/corpora/evil/`: Contains malicious or malformed datasets. Your script MUST exit with 1 for all files in this directory.

Your final solution must achieve a 100% acceptance rate on the clean corpus AND a 100% rejection rate on the evil corpus.