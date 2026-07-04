You are an AI assistant helping a researcher organize a messy sensor dataset.

The researcher has uploaded a nested archive located at `/home/user/raw_data.tar.gz`. This archive contains several zip files, which in turn contain the actual sensor log files (`.log`).

Your task is to process this raw data entirely using standard Bash utilities (no external scripts like Python required). Please perform the following steps:

1. Create a working directory at `/home/user/temp_extract/` and extract the contents of `/home/user/raw_data.tar.gz` into it.
2. Inside the extracted contents, you will find multiple `.zip` files. Extract all of these zip files.
3. Locate all the `.log` files that were extracted. 
4. Merge the contents of all `.log` files into a single master file located at `/home/user/processed_data/master.log`. 
   * CRITICAL: The files must be concatenated in strict alphabetical order of their base filenames (e.g., `A_1.log` before `A_2.log`, regardless of which directory they were extracted into).
5. Calculate the SHA256 checksum of the resulting `master.log` and save ONLY the checksum hash (the first field of the `sha256sum` output, no filenames) into `/home/user/processed_data/checksum.txt`.
6. Finally, split the `master.log` file into smaller chunks of exactly 50 lines each. Save these chunks in `/home/user/processed_data/` with the prefix `chunk_` (the files should be named `chunk_aa`, `chunk_ab`, etc., using the default alphabetic suffix of the `split` command).

Ensure that all requested directories (`/home/user/processed_data/` and `/home/user/temp_extract/`) are created if they do not exist. Clean up by deleting the `/home/user/temp_extract/` directory once you have successfully created `master.log` and the split chunks.