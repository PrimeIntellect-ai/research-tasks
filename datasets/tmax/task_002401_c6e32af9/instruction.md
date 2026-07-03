You are an AI assistant helping a researcher organize a messy dataset directory.

The researcher has a dataset located at `/home/user/dataset/`. Unfortunately, an old backup script created several cyclic symlinks (symlink loops) within this directory structure, causing standard recursive scripts to hang indefinitely. 

Your task is to write and execute a Bash script at `/home/user/scan_dataset.sh` that safely navigates the `/home/user/dataset/` directory recursively, identifying the true format of every unique, regular file while completely ignoring any symlinks (do not follow them, do not output them).

For each regular file found, your script must read the file's header (magic bytes/text) to classify it into one of four categories:
1. **ELF**: The file begins with the hex sequence `7F 45 4C 46` (the standard ELF header).
2. **WAL**: The file is a SQLite Write-Ahead Log. It begins with the hex sequence `37 7F 06 82` OR `37 7F 06 83`.
3. **GCODE**: The file is a text file where the absolute beginning of the file starts exactly with the string `;FLAVOR:`.
4. **UNKNOWN**: Any file that does not match the above signatures.

Your script must write the results to `/home/user/dataset_inventory.txt` using exactly the following format for each file:
`[absolute_file_path]: [TYPE]`

For example:
`/home/user/dataset/experiment1/data.db-wal: WAL`
`/home/user/dataset/model.gcode: GCODE`

Requirements:
- The final `/home/user/dataset_inventory.txt` file must be sorted alphabetically by the absolute file path.
- Your script must be written in Bash. 
- You must handle binary extraction and format parsing safely within the shell without executing the files.
- Run your script once it is written to generate the `dataset_inventory.txt` file.