You are tasked with building a custom incremental backup tool in Rust to help a developer organize and compress their project files. 

Create a Rust project at `/home/user/archivist`. 
The tool must compile via `cargo build` and run as a CLI application taking exactly three arguments:
`cargo run -- <source_directory> <backup_directory> <new_backup_name>`

The tool should perform the following operations:
1. **Custom Compression (RLE)**: Iterate through all `.txt` files in the `<source_directory>`. For each file, compress its contents using Run-Length Encoding (RLE). The format should represent consecutive identical characters as the decimal count followed by the character itself. For example, the string `AABBBc` becomes `2A3B1c`. This applies to all characters including newlines and spaces (e.g., `\n\n` becomes `2\n`).
2. **Incremental Backup via Hard Links**: 
   - The tool must write the compressed files to `<backup_directory>/<new_backup_name>/` with the extension `.rle` appended (e.g., `file.txt` becomes `file.txt.rle`).
   - The tool must check if a symbolic link named `current` exists in `<backup_directory>`. If it does, it points to the previous backup directory.
   - For each `.txt` file, compare its newly computed RLE content with the corresponding `.rle` file in the `current` backup. 
   - If the content is strictly identical, do not write a new file; instead, create a **hard link** from the new backup directory to the existing `.rle` file in the `current` backup.
   - If the content differs or the file didn't exist in the previous backup, write the newly compressed `.rle` file.
3. **Symbolic Link Management**: After successfully creating the new backup directory and populating it, create or update the symbolic link at `<backup_directory>/current` to point to the newly created backup directory (`<new_backup_name>`).

**Actions to Perform After Writing the Code:**
You have a set of files in `/home/user/project`. The backup directory is `/home/user/backups`.
1. Run your tool to create a backup named `backup_1`:
   `cd /home/user/archivist && cargo run -- /home/user/project /home/user/backups backup_1`
2. Append the string `ZZZZZ` to `/home/user/project/file1.txt`.
3. Run your tool again to create a backup named `backup_2`:
   `cd /home/user/archivist && cargo run -- /home/user/project /home/user/backups backup_2`

**Verification Log:**
Finally, write a shell script at `/home/user/verify.sh` that prints the inode numbers of the generated backup files in the following format, and run it to output to `/home/user/inode_log.txt`:
```
file1_b1_inode: <inode_of_backups/backup_1/file1.txt.rle>
file1_b2_inode: <inode_of_backups/backup_2/file1.txt.rle>
file2_b1_inode: <inode_of_backups/backup_1/file2.txt.rle>
file2_b2_inode: <inode_of_backups/backup_2/file2.txt.rle>
```