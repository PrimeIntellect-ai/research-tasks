You are managing the configuration backups for a legacy system. The system dumps configuration files in `ISO-8859-1` encoding into a specific directory, and you need to track these changes over time using incremental, compressed backups.

Your task is to create a Bash script `/home/user/config_tracker.sh` and perform a series of operations to prove it works.

**Phase 1: Script Development**
Write a Bash script at `/home/user/config_tracker.sh` that takes exactly three arguments:
1. `SOURCE_DIR`: The directory containing the legacy config files.
2. `STAGING_DIR`: A temporary directory for processing.
3. `BACKUP_DIR`: The directory where backup archives and metadata will be stored.

The script must perform the following actions:
1. Clear the `STAGING_DIR` if it has contents, then recreate the directory structure of `SOURCE_DIR` inside `STAGING_DIR`.
2. Find all `.conf` files in `SOURCE_DIR`.
3. Convert the character encoding of each `.conf` file from `ISO-8859-1` to `UTF-8`, saving the converted files into the exact corresponding relative paths in `STAGING_DIR`.
4. Create an incremental `tar` archive of the `STAGING_DIR` using GNU `tar`'s listed-incremental feature. 
   - The snapshot metadata file must be stored at `<BACKUP_DIR>/snapshot.snar`.
   - The archive must be gzip-compressed and saved as `<BACKUP_DIR>/backup_$(date +%s).tar.gz`. Note: Ensure there is at least a 1-second delay between script executions if you test it, to avoid overwriting tarballs.
5. Extract the list of files that were actually archived in this run by reading the newly created compressed tar stream (do not just list the staging directory) and write this list to `/home/user/latest_archived.log`.

**Phase 2: Execution and Tracking**
1. Create the following directories: `/home/user/legacy_configs`, `/home/user/staging`, and `/home/user/backups`.
2. Create a file `/home/user/legacy_configs/app.conf` encoded in `ISO-8859-1` containing the text: `téléphone=12345` (ensure the 'é' is encoded in ISO-8859-1, e.g., using `iconv`).
3. Create a file `/home/user/legacy_configs/db.conf` encoded in `ISO-8859-1` containing the text: `base_de_données=production`.
4. Make your script executable and run it using the three directories created in step 1.
5. Wait 2 seconds.
6. Modify `/home/user/legacy_configs/app.conf` by appending the line: `serveur=dédié` (again, ensure it is encoded in `ISO-8859-1`).
7. Run your script a second time.

**Verification:**
When you are finished, the automated test will inspect:
- The presence and contents of `/home/user/latest_archived.log`.
- The existence of two `.tar.gz` files and one `.snar` file in `/home/user/backups`.
- The contents of the second tarball to ensure it only contains the incrementally modified `app.conf` (and tar directory structures) and that the file inside is correctly UTF-8 encoded.