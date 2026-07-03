You are a system administrator tasked with fixing a custom data-aggregator service. The service recently failed to start because of a missing dependency issue: its configuration directory (`/home/user/app_data/active/`) contains broken, outdated, and invalid symlinks after a botched deployment. 

The application requires specific versions of configuration files to be linked in the `active` directory before it can boot. The desired state is defined in a manifest file.

Your task is to write a Bash script at `/home/user/rebuild_env.sh` that performs the following actions:

1. **Parse the Manifest:** 
   Read `/home/user/manifest.conf`. Every line in this file follows the format `link_name=target_version_file`.
   
2. **Rebuild the Directory Structure:**
   For each line in the manifest, create or update a symlink in `/home/user/app_data/active/`. The symlink should be named `link_name` and must point to the corresponding file inside `/home/user/app_data/versions/`. 
   *Note: If a symlink already exists for a given name but points to the wrong file, it must be updated.*

3. **Cleanup Stale Links:**
   Any file or symlink currently in `/home/user/app_data/active/` that is **not** listed as a `link_name` in `/home/user/manifest.conf` must be completely removed.

4. **Log the Actions:**
   As your script processes the manifest, for each successful link creation or update, it must append a line to `/home/user/rebuild.log` in exactly this format:
   `Linked <link_name> to <target_version_file>`

5. **Create a Dereferenced Backup:**
   Once the `active` directory is fully repaired, the script must create a tar.gz backup archive at `/home/user/backup/app_backup.tar.gz`.
   Crucially, the service deployment protocol requires that this backup archives the *actual files* (dereferencing the symlinks), not the symlinks themselves. Inside the tar archive, the files should appear directly under the `active/` directory (e.g., `active/db.conf`, `active/keys.json`), without the full absolute paths.

Run your script to apply the fixes and generate the backup and log file. Ensure your script is executable.