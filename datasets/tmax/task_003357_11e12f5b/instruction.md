You are an artifact manager responsible for curating a binary repository. You have a staging directory containing uncurated, raw files and need to filter, standardize, and back them up.

Please perform the following operations using standard Bash and coreutils:

1. **Metadata Search & Filter:** 
   Find all files in `/home/user/raw_artifacts` that meet **both** of the following criteria:
   - The file is executable by the user.
   - The file size is strictly greater than 100 Kilobytes (102KB or more).
   
   Copy (do not move) these matching files into `/home/user/curated_repo`.

2. **Bulk Renaming:**
   Inside `/home/user/curated_repo`, rename all the files you just copied according to these strict rules:
   - Replace any space characters in the filename with underscores (`_`).
   - Remove the existing file extension (everything from the last `.` to the end of the filename). If there is no extension, just use the original name.
   - Add the prefix `stable_` to the beginning of the filename.
   - Add the new extension `.bin` to the end.
   *(Example: a copied file named `Network Tool v2.exe` should become `stable_Network_Tool_v2.bin`)*

3. **Incremental Backup Setup:**
   - Create a full tar archive backup of the `/home/user/curated_repo` directory located at `/home/user/backup/full.tar`. 
   - You must use GNU `tar`'s listed-incremental feature to track the backup state. Save the snapshot/metadata file to `/home/user/backup/repo.snar`.

4. **Simulate Update & Incremental Backup:**
   - Create a new dummy file in the curated repository: `touch /home/user/curated_repo/stable_patch.bin`
   - Create an incremental tar backup located at `/home/user/backup/inc.tar` using the same snapshot file (`/home/user/backup/repo.snar`).

Make sure all directories exist (create them if they don't) before placing files in them. Do not use absolute paths *inside* the tar archives (use standard `tar` behavior, typically by running tar from the parent directory or using `-C`).