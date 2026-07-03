You are tasked with fixing a broken C utility and creating a Bash script that uses it to process video frames based on URL parameters. 

We have a video file located at `/app/source.mp4`.
We also have a broken C program at `/home/user/hasher.c` which is intended to read raw data from stdin and compute a custom checksum. However, it currently contains a memory safety issue (buffer overflow) that causes it to segfault on large inputs.

Your tasks are:
1. Fix the memory safety bug in `/home/user/hasher.c` and compile it to `/home/user/hasher`. Ensure it reads all bytes from standard input and outputs the custom checksum as a hexadecimal string on a single line.
2. Write a Bash script at `/home/user/process.sh` that takes a single argument: a URL string.
   - Example input: `http://localhost/api/frame?number=42`
   - The script must parse the URL to extract the value of the `number` query parameter.
   - It must use `ffmpeg` to extract that exact frame number from `/app/source.mp4` as an uncompressed raw RGB24 image (e.g., using `-vframes 1 -f image2pipe -vcodec rawvideo -pix_fmt rgb24`).
   - Note: Assume a frame rate of 24 fps if converting frame numbers to timestamps, or use ffmpeg's `select` filter (`-vf "select=eq(n\,42)"`).
   - Pipe the raw frame data directly into your compiled `/home/user/hasher` executable.
   - The Bash script must print exactly the output of the hasher to standard output, with no additional text.

Ensure your Bash script handles the parsing robustly using standard shell tools (like `grep`, `sed`, or `awk`) and sorts or diffs data if necessary, though for a single frame, it just outputs the hash.

Make sure your script is executable (`chmod +x /home/user/process.sh`). The automated testing will invoke your Bash script with various URLs to verify it behaves exactly identical to a reference implementation.