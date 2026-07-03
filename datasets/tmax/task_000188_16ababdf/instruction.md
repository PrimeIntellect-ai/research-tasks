You are tasked with building a binary curation and artifact serving system. 

You have been provided with a raw directory of submitted files in `/home/user/raw/` and an approval log in `/home/user/transactions.wal`. You also have a proprietary packing tool located at `/app/packer`.

Your goal is to parse the raw files, filter them based on the approval log and their file signatures, pack the valid ones, and serve them via a Python HTTP server.

**Step 1: Parse the WAL (Write-Ahead Log)**
Read `/home/user/transactions.wal`. This is a plain text file containing transaction records in the format:
`[YYYY-MM-DD HH:MM:SS] <ACTION> <filename>`
Where `<ACTION>` is either `APPROVE` or `REJECT`. Since files can be re-evaluated, the *last* action recorded for a specific filename dictates its final approval status. You must only process files whose final status is `APPROVE`.

**Step 2: File Format Validation**
For the approved files, read them from `/home/user/raw/`. You must strictly serve only valid ELF binaries and GCode files. Use file I/O to check their contents:
1. **ELF Binaries:** Must start with the magic bytes `\x7fELF`.
2. **GCode Files:** Must be valid text files where the first line starts with a semicolon (`;`) or an empty line, and contains at least one standard G-code command (e.g., `G0`, `G1`, `M104`, `M109`) on a new line.

**Step 3: Packing**
For every file that is both approved and valid (ELF or GCode), use the proprietary packer to compress it. The packer is a stripped binary located at `/app/packer`. 
Run it using: `/app/packer pack <input_file_path> <output_file_path>.pkg`
Save all packed artifacts (`.pkg` extension) into a new directory: `/home/user/repo/`.

**Step 4: Artifact Server**
Implement a Python HTTP server listening exactly on `127.0.0.1:8000`.
The server must expose the following endpoints:
- `GET /manifest` : Returns a JSON array of the filenames (e.g., `["firmware.elf.pkg", "case.gcode.pkg"]`) currently available in the `/home/user/repo/` directory, sorted alphabetically.
- `GET /artifact/<filename>` : Streams the requested `.pkg` file from the `/home/user/repo/` directory to the client. Return a 404 if the file does not exist.

Start the server in the background and leave it running. Write your server code in `/home/user/server.py` and run it. Do not use any external web frameworks like Flask or FastAPI; rely on Python's standard library (e.g., `http.server` or `socketserver`).