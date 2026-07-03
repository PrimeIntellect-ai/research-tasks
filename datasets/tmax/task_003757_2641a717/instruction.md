You are helping a developer organize their project files. A previous backup script failed midway, leaving a messy directory of scattered configuration files and backup archives, some of which are corrupted.

Your task is to consolidate all valid JSON configuration files into a single clean archive.

The messy files are located in `/home/user/backups/`. Inside this directory, you will find:
1. `.zip` archives (some of these are completely corrupted and cannot be extracted).
2. Loose `.json` files.

You must perform the following steps:
1. Identify all `.zip` files in `/home/user/backups/` and verify their integrity. Completely ignore any zip files that are corrupted or cannot be successfully read.
2. Extract the contents of the valid `.zip` archives.
3. Find all `.json` files (both the loose ones in `/home/user/backups/` and the ones extracted from the valid archives).
4. Verify the integrity of each `.json` file by attempting to parse it as valid JSON. Ignore any files that contain syntax errors or invalid JSON.
5. Create a new gzip-compressed tarball at `/home/user/clean_configs.tar.gz` that contains *only* the valid `.json` files. The files in the tarball must be flattened (i.e., at the root of the archive, with no subdirectories). You can assume all valid JSON files have unique filenames.
6. Create a text file at `/home/user/summary.txt` that lists the base filenames (e.g., `app_config.json`) of all the valid JSON files you included in the archive. The filenames must be sorted alphabetically, with one filename per line.

You may use bash commands and write Python scripts to accomplish this.