You are an artifact manager setting up a curation pipeline for incoming binary repositories. 

Your objective is to write a background watcher service that monitors a "dropzone" directory, validates incoming archives, renames them according to a standard convention, and moves them to their final destination using atomic file operations.

**System Requirements:**
1. The system consists of three directories:
   - `/home/user/dropzone` (incoming files)
   - `/home/user/curated` (valid, processed files)
   - `/home/user/quarantine` (corrupt or invalid files)
2. Write a watcher script (in bash, python, or language of your choice) located at `/home/user/curator`. Make it executable.
3. The script must continuously watch `/home/user/dropzone` for `.zip` and `.tar.gz` files. It must process any files already present in the directory at startup, as well as new files that arrive.
4. For each archive found:
   - **Integrity Verification:** Verify that the archive is not corrupt. `.zip` files must pass standard zip testing, and `.tar.gz` files must be valid gzip-compressed tarballs.
   - **Renaming (Valid Archives):** If the archive is valid, rename it by: 
     a) converting the entire filename to lowercase, 
     b) replacing all space characters with underscores (`_`), and 
     c) prepending `verified_` to the filename. (Example: `My Archive.zip` becomes `verified_my_archive.zip`).
   - **Atomic Placement:** Move valid, renamed archives to `/home/user/curated/`. To ensure downstream consumers do not read partial files, you MUST write/move the file into `/home/user/curated/` with a `.tmp` extension first, and then rename it to its final `.zip` or `.tar.gz` name.
   - **Quarantine (Invalid Archives):** If the archive is corrupt, move it to `/home/user/quarantine/` using its original filename (no renaming required).
5. **Shutdown Condition:** If a file named `SHUTDOWN` appears in `/home/user/dropzone`, the script must process any remaining archives, delete the `SHUTDOWN` file, and then exit cleanly.

**Execution Steps:**
1. Create your `/home/user/curator` script.
2. Run your script in the background.
3. Once running, execute the pre-existing test script: `/home/user/simulate_drops.sh`. This script will drop several archives (both valid and corrupt) into the dropzone over a few seconds, and finally drop the `SHUTDOWN` file.
4. Wait for your background script to exit.

Ensure that the final state of the `/home/user/curated` and `/home/user/quarantine` directories perfectly reflects the processed files.