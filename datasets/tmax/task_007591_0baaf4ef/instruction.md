I need help organizing and packaging some project data files for an export process that has strict size constraints. 

In the directory `/home/user/project_data`, there are several nested folders containing mixed file types. I need you to do the following using standard Bash tools:

1. Recursively find all files with a `.csv` extension inside `/home/user/project_data`.
2. Concatenate all of these `.csv` files together into a single stream. You must concatenate them in alphabetical order of their full file paths.
3. Split this concatenated data into smaller files, each containing exactly 50 lines (except possibly the last file, which may have fewer). 
4. The split files must be placed in the directory `/home/user/export_data/` (you will need to create this directory).
5. Name the split files using the prefix `part_` followed by a two-digit numeric suffix starting from `00` (i.e., `part_00`, `part_01`, `part_02`, etc.).
6. Finally, generate a SHA256 checksum manifest for all the generated chunks. Save this manifest to `/home/user/manifest.txt`. The manifest should contain the hash and the base filename (e.g., `a1b2c3d4...  part_00`), sorted alphabetically by filename. Make sure the manifest only contains the base filenames, not the full paths.

Please complete these steps. You do not need to clean up the original files.