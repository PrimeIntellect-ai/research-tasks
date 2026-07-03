You are tasked with migrating and reorganizing a large batch of legacy configuration files for a system configuration manager. 

You have been provided with a compressed archive of legacy server configurations located at `/home/user/config_backups/legacy_configs.tar.gz`. This archive contains 100 configuration files named `server_001.conf` through `server_100.conf`.

Your objective is to extract, modify, reorganize, and repackage these configurations using a Bash script.

Please complete the following steps:

1. **Extract**: Extract `/home/user/config_backups/legacy_configs.tar.gz` into the directory `/home/user/extracted_configs/`.
2. **Modify**: Write and execute a Bash script (save it as `/home/user/migrate_configs.sh`) that performs large-scale text editing on all the `.conf` files. You must update the API endpoints in all files:
   - Find lines starting exactly with `API_ENDPOINT=http://old.internal/api`
   - Replace them with `API_ENDPOINT=https://new.internal.corp/v2/api`
3. **Reorganize (Path Manipulation)**: Within your bash script, read each `.conf` file to find its timestamp (which is stored on a line like `TIMESTAMP=YYYY-MM-DD`). Move each file into a new directory structure under `/home/user/organized_configs/` based on its year and month. 
   - For example, if `server_042.conf` has `TIMESTAMP=2023-05-12`, it should be moved to `/home/user/organized_configs/2023/05/server_042.conf`.
4. **Repackage**: Once all files are modified and moved, compress the `organized_configs` directory into a new gzip-compressed tar archive located at `/home/user/migrated_configs.tar.gz`. The archive should contain the `YYYY/MM/server_XXX.conf` structure directly (do not include the `organized_configs` parent directory itself in the archive paths; the root of the archive should be the year directories).
5. **Manifest**: Generate a manifest file at `/home/user/migration_manifest.txt` containing the exact list of `.conf` file paths as they appear inside the new `migrated_configs.tar.gz` archive. The paths should be relative (e.g., `2022/01/server_001.conf`) and must be sorted alphabetically.

Ensure your Bash script `/home/user/migrate_configs.sh` is executable and can be run to perform steps 2 and 3. Do not use root privileges.