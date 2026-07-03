I need you to help me organize a messy project directory containing large assets, logs, and custom binary data. Many files are duplicated, wasting space, and they are all mixed together in `/home/user/project_dump`.

Please perform the following operations:

1. **Deduplication via Hard Links**: 
   Analyze all files in `/home/user/project_dump`. If any files have exactly identical content, keep the file with the lexicographically first name as the "base" file, and replace the duplicates with a **hard link** to the base file. This will save space without breaking paths.

2. **Binary Header Extraction & Categorization**:
   Inspect the first 4 bytes (magic number) of every *unique* file to determine its type:
   - If it starts with `89 50 4E 47` (hex), it is an image.
   - If it starts with `DA 7A BE EF` (hex), it is a custom data file.
   - If it starts with `45 52 52 20` (hex, which is ASCII "ERR "), it is a log file.
   *(Assume all files in the directory match one of these three signatures).*

3. **Symlink Organization**:
   Create a new directory `/home/user/organized_assets/` containing three subdirectories: `image`, `custom`, and `log`.
   For each *base* file (ignoring the deduplicated hard links), create a **symbolic link** in the corresponding subdirectory pointing to the base file in `/home/user/project_dump`. The symlink should have the same name as the base file.

4. **Atomic Index Generation**:
   Generate a JSON index file containing metadata about the base files. 
   Write this file to `/home/user/organized_assets/index.json` **atomically** (i.e., write to a temporary file first, then perform an atomic rename/move to the final path, so the file is never read in an incomplete state).
   
   The JSON file must be an array of objects, strictly sorted alphabetically by the base file name. Each object must have this exact format:
   ```json
   [
     {
       "file": "asset_01.bin",
       "type": "image",
       "hardlinks": 2
     },
     ...
   ]
   ```
   *Note: `hardlinks` should reflect the total number of hard links the base file has after your deduplication step.*

Write a script (in any language you prefer, e.g., Python, Bash) to automate this process. Make sure your script handles large files efficiently by streaming or just reading the required header bytes, rather than loading entire multi-gigabyte files into memory.