You are a storage administrator managing disk space on a Linux server. A rogue backup script has created a mess in `/home/user/storage_dump`, generating a chaotic hierarchy with deep symlinks, some of which form infinite loops. Many files are useless junk, but there are valuable ELF binaries and 3D printer GCode files scattered throughout, some hidden behind valid symlinks.

Your task is to write and execute a Go program that traverses `/home/user/storage_dump` following symlinks, but gracefully handles and avoids infinite symlink loops. 

During the traversal, your program must examine the contents of every unique regular file to determine its type based on file headers, ignoring file extensions completely:
1. **ELF Binaries**: The first 4 bytes are exactly `\x7FELF`.
2. **GCode Files**: The first 4 bytes are exactly `; G-`.

For your disk space analysis, you must generate a CSV report at `/home/user/report.csv`. 
To ensure you aren't double-counting files that are symlinked multiple times, track files by their underlying `inode` number. The report must contain exactly the unique valid files found (one entry per unique inode).

The CSV format must be exactly:
```csv
inode,type,size
```
Where:
- `inode` is the integer inode number of the real underlying file.
- `type` is either `ELF` or `GCODE`.
- `size` is the file size in bytes.

The output lines must be sorted numerically by the `inode` in ascending order. Do not include a CSV header row in the final output file.

Requirements:
- Your Go program must be saved at `/home/user/scanner.go` and executed to produce `/home/user/report.csv`.
- You must write the traversal logic to follow symlinks to directories and files, but you must prevent infinite loops (e.g., by tracking visited directory inodes).
- Only include ELF and GCODE files in the report. Ignore all other files.