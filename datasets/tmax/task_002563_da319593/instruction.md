You are an AI assistant helping a researcher organize their dataset. 

The researcher has an archive located at `/home/user/research_data.tar`. This archive contains some messy data that needs to be cleaned up for a new processing pipeline. Unfortunately, the archive contains a symlink loop that has been breaking the researcher's automated backup scripts, and the text files have outdated encodings and poorly formatted names.

Your task is to perform the following cleanup operations:
1. Extract the contents of `/home/user/research_data.tar` into a new directory: `/home/user/processed/`.
2. Find and delete any symlinks within `/home/user/processed/` to prevent infinite loop issues during future backups.
3. The dataset contains several text files (`*.txt`). They are currently encoded in `ISO-8859-1`. Convert the contents of all `.txt` files in the extracted directory to `UTF-8`.
4. Bulk rename all the `.txt` files in `/home/user/processed/` (and its subdirectories) by replacing any space characters (` `) in their filenames with underscores (`_`).
5. Generate a final inventory of the cleaned text files. Compute the SHA256 checksum for each `.txt` file. Write the results to `/home/user/final_inventory.txt`. 

The format of `/home/user/final_inventory.txt` must exactly match the standard output of the `sha256sum` command (e.g., `<hash>  <filepath>`), using the absolute paths to the files. Sort the lines alphabetically by filepath.

You may use any Bash commands or write short shell scripts to accomplish this.