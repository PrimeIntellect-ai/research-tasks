You are a backup administrator tasked with archiving data and securing the backup infrastructure after a recent security breach. The attacker attempted to compromise the backup restoration process using an archive extraction vulnerability (similar to "Zip Slip"), and they also physically breached the server room.

Your task consists of two parts:

**Part 1: Manifest Sanitiser (Adversarial Corpus)**
Our backup system uses a custom, multi-line text format for its archive manifests (`.manifest`). The attacker modified some manifests to include path traversals in order to overwrite system files during backup extraction.
A manifest file consists of multiple records separated by blank lines. Each record looks like this:
```
[RECORD]
ID: 8945
File-Path: documents/finances.csv
Size: 4509
[END]
```

You must write a robust detector script at `/home/user/detect_slip.sh` (you may use Bash, Python, or any installed language, but the entrypoint must be this executable shell script or have the correct shebang).
- The script will be invoked as: `/home/user/detect_slip.sh <path_to_manifest_file>`
- It must parse the manifest and check the `File-Path:` field of every record.
- **Clean files**: If all `File-Path` values are strictly relative to the extraction base directory and NEVER traverse outside of it (e.g., `folder/file.txt`, `a/b/../c.txt` which resolves to `a/c.txt`), your script must print `CLEAN` to stdout and exit with status code `0`.
- **Evil files**: If ANY `File-Path` attempts to write outside the base directory (e.g., absolute paths like `/etc/passwd`, or relative traversals that escape the root like `../bin/sh`, or `folder/../../secret`), your script must print `EVIL` to stdout and exit with status code `1`.
Your solution will be evaluated against a hidden corpus of clean and evil manifests. It must correctly classify 100% of both corpora.

**Part 2: Video Artefact Analysis**
We have recovered a video from the server room's security camera during the time of the breach, located at `/app/backup_cam.mp4`.
When the attacker triggered the room's physical alarm, a bright red strobe light flashed. You must use `ffmpeg` (and any other CLI tools or scripts you prefer) to perform a per-frame analysis of this video. 
Count the exact number of frames where the strobe light is active (defined as a frame where the image is predominantly solid red; you can isolate frames where the red channel is extremely high and green/blue are negligible).
Write the final integer count of these red frames to `/home/user/red_frame_count.txt`.

Ensure your script is executable (`chmod +x /home/user/detect_slip.sh`) and handles edge cases in path resolution.