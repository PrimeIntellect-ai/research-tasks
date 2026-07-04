You are assisting a technical writer who is organizing a repository of 3D printing documentation. Authors submit their tutorials as a combination of a video demonstration and a tarball archive containing GCode and text files. 

Recently, the team discovered that some submitted tarballs are maliciously crafted. When extracted, they exploit "Tar Slip" vulnerabilities by using absolute paths or parent directory traversals (`../`) to overwrite system files outside the target extraction directory.

Your task is to build a robust checking mechanism and process a sample submission:

1. **Archive Sanitizer**: 
   Create a Bash script at `/home/user/check_tar.sh` that takes exactly one argument: the path to a `.tar` archive.
   - The script must inspect the paths inside the archive **without extracting it**.
   - If any file or directory path within the archive is absolute (starts with `/`) or contains a directory traversal component (`../`), the script must print `REJECT` to standard output and exit with status code `1`.
   - If all paths are safe, the script must print `ACCEPT` and exit with status code `0`.
   - The script should only use standard Bash built-ins and standard coreutils/tar commands.

2. **Video Thumbnail Extraction**:
   There is a sample video tutorial located at `/app/demo_video.mp4`. 
   - Extract a single frame at exactly the 2-second mark (00:00:02) from this video.
   - To prevent corrupted reads by other processes, write the extracted frame to a temporary file first, and then use an atomic move operation to place the final image at `/home/user/thumbnail.jpg`.
   - You may use `ffmpeg` for this extraction.

Ensure your `check_tar.sh` script is executable. You can test your script on any dummy tar files you create. An automated test suite will later run your script against a hidden corpus of clean and malicious archives to verify its accuracy.