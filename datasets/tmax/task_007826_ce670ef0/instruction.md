You are assisting a network engineer in troubleshooting and automating the backup of network router configurations. The previous backup system has been failing due to timezone mismatches causing filename collisions, and backups failing when the remote mount point changes. 

Your objective is to write a Python script at `/home/user/process_backups.py` that reliably packages the configurations, calculates their storage footprint, handles the timezone correctly, and dynamically determines the backup destination from a simulated fstab file.

Write the script to perform the following steps:

1. **Fstab Configuration Parsing**:
   Read the file `/home/user/network_fstab` (which uses the standard `/etc/fstab` format). Find the entry where the device/filesystem is exactly `//192.168.1.100/net_backups`. Extract its corresponding mount point.

2. **Storage Monitoring**:
   Calculate the total size in bytes of all `.cfg` files located directly inside `/home/user/router_configs/`. Do not include subdirectories or other file types.

3. **Timezone Configuration**:
   Determine the current time in the `Asia/Tokyo` timezone. Format this time as `YYYY-MM-DD_HH-MM-SS`.

4. **Backup Execution**:
   Create a compressed tarball (`.tar.gz`) containing all the `.cfg` files from `/home/user/router_configs/`. 
   Save this archive inside the mount point directory you extracted in Step 1.
   The filename must exactly match the format: `backup_<TIME_IN_TOKYO>_tokyo.tar.gz` (e.g., `backup_2023-10-25_14-30-05_tokyo.tar.gz`).

5. **Logging**:
   Create a log file at `/home/user/backup_summary.log` with exactly the following three lines (replace the bracketed placeholders with your calculated values):
   ```
   Mount: <extracted_mount_point_absolute_path>
   Size: <total_size_of_cfg_files_in_bytes>
   Archive: <absolute_path_to_the_tar_gz_file>
   ```

Ensure your script is executable (`chmod +x /home/user/process_backups.py`) and run it so that the log file and the archive are generated. You may use Python's built-in modules (like `tarfile`, `os`, `datetime`, `zoneinfo`, etc.).