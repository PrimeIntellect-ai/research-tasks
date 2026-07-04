You are an artifact manager tasked with curating a queue of binary build repositories. An automated builder is dumping compressed build artifacts into the `/home/user/incoming/` directory. Each file is a `.tar.gz` archive containing a `metadata.txt` file and a large `payload.bin` file.

You must write a Python script at `/home/user/curate.py` that processes all `.tar.gz` files in `/home/user/incoming/` according to the following strict rules:

1. **Compressed Stream Processing**: You must read the `metadata.txt` file from within each `.tar.gz` archive directly from the compressed stream. Do not extract the archives to disk (e.g., do not use `tar -xzf` to a temp folder), as the `payload.bin` files are conceptually too large for the disk quota. 

2. **Metadata Extraction**: Inside `metadata.txt`, there are two lines you need to extract:
   `Build-ID: <id>`
   `Date: <YYYY-MM-DD>`

3. **Path Manipulation and Bulk Renaming**: Move and rename each processed archive into a structured repository at `/home/user/repo/`. The target directory structure must be organized by year and month, and the file renamed to the Build-ID. 
   Format: `/home/user/repo/<YYYY>/<MM>/<Build-ID>.tar.gz`
   Create the necessary directories if they do not exist.

4. **Atomic Index Update**: Maintain a central JSON index at `/home/user/repo/manifest.json`. Every time you process an artifact and move it, you must add its entry to `manifest.json`. 
   The format of `manifest.json` must be a JSON array of objects, sorted chronologically by Date (earliest first), like so:
   ```json
   [
     {"date": "2023-10-01", "build_id": "ABC1", "path": "/home/user/repo/2023/10/ABC1.tar.gz"},
     ...
   ]
   ```
   **Crucial Constraint**: A background log-rotation and monitoring process is constantly reading `manifest.json`. You *must* update this file using an **atomic write**. This means you must write the updated JSON array to a temporary file (e.g., `manifest.json.tmp`) and then atomically replace the original file (e.g., using `os.replace()` in Python or `mv` in bash) to avoid race conditions and corrupted reads.

Execute your script to process all current files in `/home/user/incoming/`. Ensure the final `/home/user/repo/manifest.json` correctly reflects all moved artifacts.