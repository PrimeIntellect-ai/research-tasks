I am a researcher working with a large dataset of simulated brain scans. The dataset was recently transferred from an old server, and I suspect some of the files were corrupted during the process. I need your help to filter out the corrupted files, safely copy the valid ones to a new directory, and generate a manifest for my incremental backup system.

The raw dataset is located at `/home/user/raw_dataset`. It contains multiple nested directories with `.dat` files. 

Valid scan files always begin with a specific 4-byte magic number: `BRAN` (in ASCII/UTF-8, which is `0x42 0x52 0x41 0x4E` in hex). Corrupted or incomplete files will have different headers.

Please write and execute a Python script that does the following:
1. Recursively traverses the `/home/user/raw_dataset` directory.
2. Reads the binary header (first 4 bytes) of every `.dat` file to determine if it is valid.
3. For every valid file, copies it to `/home/user/clean_dataset/` while preserving the exact relative directory structure.
4. To prevent partial writes in case of a crash, the copy operation must be atomic. Specifically, write the copied data to a temporary file (e.g., appended with `.tmp`) in the destination directory, and then rename it to the final `.dat` filename.
5. Finally, generate a CSV manifest file at `/home/user/backup_manifest.csv` that will be used for differential backups. The CSV should not have a header row. Each line must contain the relative path of the valid file (relative to the `clean_dataset` root) and its file size in bytes, separated by a comma (e.g., `subject1/scan.dat,1048576`). Sort the lines alphabetically by the relative path.

Ensure your script handles the directory creation in the target path gracefully. Let me know once the script has finished executing and the `backup_manifest.csv` is generated.