You are helping a developer organize a dump of old project files that were archived using a bizarre, custom "compression" script to save them from being indexed by search tools. 

You have been provided an archive located at `/home/user/project_dump.tar.gz`.

Inside this archive are several files with the extension `.txt.cst`. They have been obfuscated using the following custom compression method:
1. Every line in the original text was reversed.
2. The entire resulting text was then Base64 encoded.

Your task is to write and execute a Bash script (or series of shell commands) to do the following:
1. Extract `/home/user/project_dump.tar.gz` into a temporary directory.
2. For each `.txt.cst` file, reverse the custom compression (decode the Base64, then reverse the lines back to normal).
3. The original files contain a mix of lines. Use `sed` or `awk` to extract *only* the lines that begin with the exact string `[KEEP] `.
4. Remove the `[KEEP] ` prefix from those extracted lines.
5. Save the cleaned up files into a new directory `/home/user/organized/`, keeping the same base filename but changing the extension to `.txt` (e.g., `data.txt.cst` becomes `data.txt`).
6. Finally, compress all the resulting `.txt` files into a single zip archive at `/home/user/organized_files.zip`. The zip archive must contain *only* the `.txt` files at the root of the archive (do not include the `/home/user/organized/` directory structure inside the zip).

Ensure your final zip file is correctly formatted and located exactly at `/home/user/organized_files.zip`.