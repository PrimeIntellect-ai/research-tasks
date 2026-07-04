You are an AI assistant helping a technical writer automate their documentation pipeline. The writer is dealing with a legacy system that dumps raw binary documentation logs into a directory, and they need a robust, automated way to process these files as they arrive.

Your task is to build a two-part Python-based automation pipeline: a core parser and a directory watcher.

### Phase 1: The Core Parser
We have an architecture diagram saved at `/app/diagram.png`. Somewhere in this image, there is a text label that specifies the "Record Magic Marker" used by our legacy system (it looks like `MARKER: <SOME_STRING>`). You need to find this string.

Write a Python script at `/home/user/parse_single.py` that acts as a Unix-style filter. It must:
1. Read a binary stream from `stdin` (using streaming or memory-mapped I/O to handle potentially large inputs efficiently).
2. Scan the stream for records. A record strictly consists of:
   - The Magic Marker string (encoded in ASCII) extracted from the image.
   - Immediately followed by a 4-byte unsigned little-endian integer representing the length `L` of the payload.
   - Immediately followed by `L` bytes of UTF-8 encoded text payload.
3. For each successfully parsed record, extract the text payload, replace all exact occurrences of the word "DRAFT" with "FINAL", strip any trailing whitespace from the payload, and print it to `stdout` followed by a single newline `\n`.
4. Ignore any bytes between records that do not match the valid structure.

### Phase 2: The Watcher & Processor
Write a second Python script at `/home/user/watcher.py` that:
1. Continuously watches the directory `/home/user/incoming/` for new files (you can use simple polling or `inotify`).
2. When a new `.bin` file appears, it processes the file using your `parse_single.py` logic.
3. It must write the processed output to `/home/user/processed/<filename_without_ext>.txt`.
4. **Safety requirement:** The write must be atomic. Write to a temporary file first, then move it into place so partial writes are never visible in the `/home/user/processed/` directory.
5. **Link management:** After a successful atomic write, update a symbolic link at `/home/user/processed/latest.txt` to point to the newly processed text file.

### Setup and Constraints
- Create the directories `/home/user/incoming/` and `/home/user/processed/` before running your watcher.
- Ensure your `parse_single.py` is executable (`chmod +x`).
- Do not use any external dependencies outside of the standard library and `pytesseract`/`Pillow` for reading the image.
- Leave `watcher.py` running in the background or demonstrate its functionality clearly.