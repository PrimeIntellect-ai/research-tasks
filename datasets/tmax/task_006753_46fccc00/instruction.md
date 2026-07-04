You are an artifact manager for a binary repository. We have a set of incoming software artifacts in a staging directory, and we need to curate them concurrently, filter them based on internal metadata, and convert the approved ones to a standard format.

The incoming artifacts are located in `/home/user/staging/`. They are a mix of `.zip`, `.tar.gz`, and `.tar.bz2` files. 

Your task is to write a Python script `/home/user/curate.py` and run it concurrently using bash to process these archives. 

**Script Requirements (`/home/user/curate.py`):**
1. **Input**: The script must take exactly one argument: the absolute path to an archive file.
2. **Metadata Search**: The script must read the contents of `meta.json` located at the root inside the archive (without fully extracting the archive to disk if possible, though temporary extraction is allowed).
3. **Filtering**: If the `meta.json` contains the key `"author"` with the value `"alice"`, the artifact is approved for curation. Otherwise, the script should exit silently without doing anything.
4. **Format Conversion**: For approved artifacts, repackage all contents of the original archive into a new, uncompressed `.tar` file in `/home/user/curated/`. The new filename should be the original filename with its extensions removed and `.tar` appended (e.g., `app_v1.tar.gz` becomes `app_v1.tar`).
5. **Concurrency & File Locking**: After successfully curating an artifact, the script must append a JSON-lines record to `/home/user/curated/manifest.jsonl`. Because we will run this script concurrently, **you must use `fcntl.flock`** to acquire an exclusive lock on the manifest file before appending to ensure no data corruption occurs. 
   The appended JSON must have exactly this format:
   `{"original": "<basename_of_original_archive>", "curated": "<basename_of_new_tar>", "build": <build_number_from_meta_json>}`

**Execution:**
Once the script is written, make sure the `/home/user/curated/` directory exists. Then, execute your script concurrently against all files in `/home/user/staging/` using up to 4 parallel processes. You can do this using standard bash tools like `find` and `xargs`.

**Verification:**
An automated test will inspect `/home/user/curated/manifest.jsonl` to ensure it contains the correct records and was not corrupted by concurrent writes. It will also inspect the `.tar` files in `/home/user/curated/` to verify format conversion.