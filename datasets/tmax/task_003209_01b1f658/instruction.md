You are a storage administrator managing video logs and archiving disk space. You have two main objectives:

Part 1: Video Processing
A surveillance video is located at `/app/camera_01.mp4`. 
1. Create a directory `/home/user/frames/`.
2. Extract 1 frame per second from `/app/camera_01.mp4` using `ffmpeg`. Name them `frame_001.jpg`, `frame_002.jpg`, etc.
3. Archive the extracted frames into a tarball at `/home/user/reference_frames.tar.gz`. Make sure the tarball contains just the JPEG files at its root (no parent directories).

Part 2: Archive Sanitization
Because our log rotation script sometimes races with the writing process, we occasionally get corrupted archives. Furthermore, we need to ensure that archives uploaded by users do not contain malicious symlinks that could overwrite critical system files when extracted.

You must write a Bash script at `/home/user/verify_archive.sh`. This script will be invoked with a single argument: the path to a `.tar.gz` archive.

Your script must determine if the archive is safe ("CLEAN") or corrupted/malicious ("EVIL"). 
An archive is considered "EVIL" if:
- It contains any symlinks (either absolute or relative) that would resolve to a path outside the directory it is extracted into.
- It contains any file or directory with the exact name `lock` or `.lock` (which indicates it was archived during an incomplete write).
- The tarball itself is corrupted or cannot be read.

If the archive is safe, your script must:
- Print exactly `CLEAN` to standard output.
- Exit with status code `0`.

If the archive violates any safety rules, your script must:
- Print exactly `EVIL` to standard output.
- Exit with status code `1`.

To help you develop and test your script, we have provided two directories containing sample archives:
- `/app/corpora/clean/` contains safe archives.
- `/app/corpora/evil/` contains unsafe archives.

Your final `/home/user/verify_archive.sh` will be tested against these corpora (as well as hidden grading sets). It must achieve 100% accuracy.