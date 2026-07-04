I need you to write a Bash script to organize and filter our project backup files. We recently had an issue where our backup script followed malicious symlinks into infinite loops, and some files have corrupted binary headers. 

I have created a test environment with a set of backup files. Your task is to write a Bash script named `/home/user/filter_backups.sh` that takes an input file path as an argument and exits with code 0 if the file is "clean" and code 1 if it is "evil" (corrupted, malicious, or invalid).

Here are the rules for determining if a file is clean:
1. **Magic Bytes:** The file must start with one of the allowed binary magic signatures. I don't have the list of allowed signatures in text, but there is a screenshot of the policy document located at `/app/magic_signatures.png`. You will need to extract the hex signatures from this image (e.g., using `tesseract`).
2. **Symlink Safety:** If the file is a symlink, it must resolve to a valid file within the same base directory without causing an infinite loop. You must safely detect symlink loops.
3. **Processing Requirements:** Your script must use standard stream redirection and temp files safely. If you need to write temporary data to inspect headers, you must use atomic writes (e.g., writing to a temp file and moving it) to prevent race conditions during parallel processing.

The script should accept a single argument: the full path to a file to inspect.
Example invocation: `/home/user/filter_backups.sh /path/to/file`
Exit code 0: Clean file.
Exit code 1: Evil file.

Please write the robust Bash script to satisfy these conditions. Automated tests will run your script against a large corpus of both clean and evil files.