You are an artifact manager tasked with curating a messy repository of binary files. The raw repository located at `/home/user/artifacts_raw` contains a mix of valid binaries, misnamed files, hard links, broken symbolic links, and symbolic links that form infinite loops.

Your goal is to write and execute a Bash script that processes this directory, extracts the true file types from their binary headers, safely handles links, and copies the deduplicated, correctly named files to a new directory `/home/user/artifacts_curated`.

Here are your specific requirements:

1. **Link Cleanup & Handling:**
   - Detect and ignore/delete any broken symbolic links and any symbolic links that form infinite loops in `/home/user/artifacts_raw`.
   - Resolve valid symbolic links to their targets.
   - Deduplicate files that have identical content (e.g., hard links or copies) so that only one copy of each unique file is placed in the curated directory.

2. **Binary Header Extraction:**
   - Do not rely on existing file extensions. You must determine the file type by reading the first few bytes (magic number) of each valid file.
   - Map the headers to the following extensions:
     - Starts with hex `7f 45 4c 46` -> `.elf`
     - Starts with hex `89 50 4e 47` -> `.png`
     - Starts with hex `1f 8b` -> `.gz`
     - Starts with hex `50 4b 03 04` -> `.zip`
   - If a file does not match any of these signatures, assign it the `.bin` extension.

3. **Bulk Renaming & Curation:**
   - Create the directory `/home/user/artifacts_curated`.
   - Copy each unique valid file into this directory.
   - The new filename must be the SHA-256 hash of the file's contents, followed by the correct extension determined in step 2. (Format: `<sha256hash>.<extension>`).

4. **Manifest Generation:**
   - Create a log file at `/home/user/curation_manifest.txt`.
   - For every unique file curated, append a line with the format: `<sha256hash> <extension>`.
   - Sort the manifest alphabetically by the SHA-256 hash.

Write the Bash script, execute it, and ensure the `/home/user/artifacts_curated` directory and the `/home/user/curation_manifest.txt` file are perfectly formatted.