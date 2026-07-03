You are tasked with fixing a broken configuration backup processing pipeline. The previous configuration manager left a script that constantly crashes because it gets stuck in infinite symlink loops. You need to write a robust Bash script from scratch to process these configuration archives safely.

Write a Bash script at `/home/user/process_configs.sh` that does the following:

1. **Safely Find Archives:** Scan the directory `/home/user/config_backups` for all `.tar.gz` files. The directory contains several symlink loops (e.g., symlinks pointing to each other or to parent directories). Your script MUST NOT follow symlinks.
2. **Verify Archive Integrity:** Some of the `.tar.gz` files are corrupted. Check the integrity of each archive (e.g., using `tar -tzf`). Only process archives that pass the integrity check.
3. **Extract and Parse Data:** Extract the valid archives into a temporary staging area. Inside these archives are text files containing configuration data. The files have arbitrary names (like `data_8472.txt`). Each file contains metadata in its first 5 lines, specifically looking like:
   `# ENV: <environment_name>`
   `# SERVICE: <service_name>`
4. **Bulk Rename and Move:** For every extracted file, read the environment and service names. Move the file into `/home/user/processed_configs/` and rename it using the format:
   `<environment_name>_<service_name>_<original_filename>.conf`
   If a file does not have both the `# ENV:` and `# SERVICE:` tags in the first 5 lines, skip it and do not copy it. Convert any spaces in `<environment_name>` or `<service_name>` to underscores during renaming.
5. **Generate Manifest:** Finally, generate a standard SHA256 checksum manifest of all the successfully renamed files in the `/home/user/processed_configs/` directory. Save this manifest as `/home/user/processed_configs/manifest.sha256`. The manifest should only contain the basenames of the files, not full paths.

Make sure your script is executable (`chmod +x /home/user/process_configs.sh`) and run it so the final state is achieved. Create `/home/user/processed_configs/` if it doesn't exist.