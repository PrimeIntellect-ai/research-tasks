You are a storage administrator managing disk space and incident response. A junior admin intercepted a suspicious archive that appeared designed to perform a "Zip Slip" directory traversal attack. To be safe, they extracted it into a raw disk image, `/home/user/suspect_data.img` (ext4 format), instead of the live filesystem. 

Your task is to analyze this data without root access, extract the critical logs, and generate a report.

Follow these steps exactly:
1. Create a mount point at `/home/user/mnt`.
2. Since you do not have root access, mount the ext4 image `/home/user/suspect_data.img` to `/home/user/mnt` using a user-space mounting tool (`fuse2fs`).
3. Inside the mount, navigate to `mnt/payload/`. You will find deeply nested directories containing fragmented log files named like `[servicename].log.chunk[N]` (where N is an integer).
4. Write a Python script to group these chunks by their base service name and merge them in ascending order of their chunk number into single files (e.g., `[servicename].merged.log`). Store these merged logs in `/home/user/merged_logs/`.
5. The merged logs are in a corrupted JSON Lines format. Due to a buggy logger, all JSON objects use single quotes (`'`) instead of double quotes (`"`), and they have a trailing `!!!` at the end of every line.
6. Using Python, parse these merged files, fix the formatting on-the-fly, and extract all log entries where the `'level'` is exactly `'FATAL'`.
7. Write the extracted FATAL entries as valid, standard JSON Lines (double quotes, no trailing `!!!`) to `/home/user/fatal_alerts.jsonl`. Each line must contain only the following keys: `"timestamp"`, `"service"`, and `"message"`.
8. Once finished, gracefully unmount the directory using `fusermount -u /home/user/mnt`.

Ensure your Python scripts handle the data robustly and rely only on standard libraries. Your final output must strictly be in `/home/user/fatal_alerts.jsonl`.