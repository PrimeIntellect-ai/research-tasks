You are assisting a technical writer in organizing their scattered Markdown documentation into a compressed archive format, while ensuring concurrent safety for future automation.

You are provided with the following environment:
1. A configuration file located at `/home/user/archiver.conf` which contains key-value pairs, including the destination directory: `DEST_DIR=/home/user/archive`
2. A source directory `/home/user/drafts` containing various `.md` files scattered across multiple nested subdirectories.
3. A custom compression Python script `/home/user/compress.py` that reads raw text from `stdin`, applies zlib compression followed by base64 encoding, and writes the result to `stdout`.

Your task is to write and execute a Bash script at `/home/user/process.sh` that performs the following operations:
1. Extract the `DEST_DIR` path from `/home/user/archiver.conf` and ensure the directory exists.
2. Find all `.md` files within `/home/user/drafts` (including all subdirectories).
3. For each `.md` file found:
   a. Pipe its contents through `python3 /home/user/compress.py`.
   b. Redirect the output to a new file in the `DEST_DIR`. The new file must be named `<original_basename>.z64` (e.g., if processing `intro.md`, output should go to `/home/user/archive/intro.z64`).
   c. Append a record to `/home/user/archive/manifest.txt` in the exact format: `[ARCHIVED_FILENAME]:[FULL_ORIGINAL_FILEPATH]`. (e.g., `intro.z64:/home/user/drafts/section1/intro.md`).
   d. CRITICAL: You must use Linux file locking (`flock`) when writing to `/home/user/archive/manifest.txt` to ensure that if multiple instances of this script were run concurrently, the manifest would not be corrupted.

Run your script to process the files. Ensure the manifest file correctly lists all processed files.