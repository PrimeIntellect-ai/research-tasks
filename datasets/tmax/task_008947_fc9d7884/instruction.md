You are tasked with organizing a set of legacy project files for a developer. The files are currently compressed in an archive and have inconsistent naming conventions and formats.

Here are the specific steps you must perform:

1. **Extraction**: Extract the contents of the archive `/home/user/legacy_project.tar.gz` into a new directory `/home/user/project`. 
2. **Bulk Renaming**: All files inside the extracted `/home/user/project` directory begin with the prefix `dev_`. Rename all these files to remove the `dev_` prefix (e.g., `dev_config.csv` should become `config.csv`).
3. **Format Conversion**: Using Python, find all `.csv` files in `/home/user/project` and convert them into `.json` format. The resulting JSON files should be an array of objects (dictionaries), where the keys are the column headers from the CSV. Save them with the `.json` extension in the same directory and delete the original `.csv` files.
4. **Compressed Stream Processing**: There is a compressed log file now located at `/home/user/project/server_logs.gz` (after renaming). Using Python, process this compressed stream without fully extracting it to disk. Find all lines containing the string `CRITICAL` and write those lines to a new plaintext file at `/home/user/project/critical_errors.txt`.
5. **Symbolic Link Management**: Create a directory `/home/user/public_html/assets`. Inside this new directory, create symbolic links pointing to all `.png` files located in `/home/user/project`. The symbolic links must have the exact same base names as the target files (e.g., `background.png` linking to `/home/user/project/background.png`). Ensure you use absolute paths for the symlink targets.

You may use bash commands, Python scripts, and standard Linux utilities to complete this task. Create any intermediate scripts as needed in `/home/user/`.

Verify your final setup matches the instructions perfectly before finishing.