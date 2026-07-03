You are an AI assistant helping a developer organize a messy project directory into a structured archive. 

You need to write a multi-language solution (e.g., a combination of Python and shell commands) to process files in `/home/user/workspace/raw_data/` according to a configuration file located at `/home/user/workspace/rules.json`.

Here are your instructions:

1. **Read the Configuration:**
   Parse the JSON file at `/home/user/workspace/rules.json`. It contains three arrays of filenames: `"datasets"`, `"binaries"`, and `"logs"`.

2. **Process Datasets (CSV):**
   For each file listed in the `"datasets"` array, read the corresponding CSV file from `/home/user/workspace/raw_data/`. Using streaming or chunked I/O (to handle potentially large files efficiently without loading the whole file into memory), filter out any rows where the `status` column exactly matches `"ERROR"`. Write the cleaned data to a new CSV file with the same name in `/home/user/workspace/organized/datasets/`. Keep the header intact.

3. **Process Binaries (ELF):**
   For each file listed in the `"binaries"` array, determine its machine architecture by parsing its ELF header (you may use system tools like `readelf`, `file`, or write custom parsing logic). 
   - Create directories `/home/user/workspace/organized/binaries/x86_64/` and `/home/user/workspace/organized/binaries/other/`.
   - If the ELF file is for the `x86-64` (or `x86_64`) architecture, create a **hard link** to it in the `x86_64` directory.
   - If it is any other architecture (or not a valid ELF), create a **hard link** to it in the `other` directory.

4. **Process Logs:**
   For each file listed in the `"logs"` array, create a **symbolic link** in `/home/user/workspace/organized/logs/` pointing to the original file in `/home/user/workspace/raw_data/`.

5. **Create the Archive:**
   Once the `/home/user/workspace/organized/` directory is fully populated, compress the entire `organized` directory into a tarball at `/home/user/workspace/archive.tar.gz`. Make sure symlinks are preserved as symlinks in the archive, and hardlinks are preserved as hardlinks.

**Requirements:**
- All destination directories must be created by your script.
- Ensure that the final archive `archive.tar.gz` is well-formed.
- You can install any standard packages (e.g., `python3`, `readelf` via `binutils`, etc.) if they are not present.