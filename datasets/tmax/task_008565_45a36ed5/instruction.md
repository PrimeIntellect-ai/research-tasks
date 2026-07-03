I am a researcher organizing a large collection of text-based datasets located in `/home/user/raw_data`. Unfortunately, a legacy backup tool crashed and created several recursive symlinks within this directory, causing standard traversal tools to get stuck in infinite loops. 

I need you to write a Bash script located at `/home/user/compile_dataset.sh` to safely extract the valid data from these files.

Here are the exact requirements for the script:
1. **Safe Traversal**: It must search for all files ending in `.dat` inside `/home/user/raw_data`, effectively ignoring/handling any symlink loops so the script doesn't hang.
2. **Data Filtering**: For each `.dat` file found, extract only the lines that begin exactly with the string `[RETAIN]`. 
3. **Stream Processing & Atomic Writes**: The final output must be saved to `/home/user/clean_dataset.txt`. However, to prevent partial data corruption if the script is interrupted, your script MUST write the filtered output to a temporary file first (created securely via `mktemp`). 
4. **Deterministic Output**: The final collected lines must be sorted alphabetically in the final output file.
5. **Finalization**: Once all processing and sorting is complete, atomically rename the temporary file to `/home/user/clean_dataset.txt`.

Please write and execute this script. I will verify your success by checking the contents of `/home/user/clean_dataset.txt` and ensuring your script correctly uses temporary files and atomic moves. Make sure the script is executable.