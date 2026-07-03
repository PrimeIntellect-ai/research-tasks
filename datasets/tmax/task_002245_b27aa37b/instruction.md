You are acting as a storage administrator. Disk space is running dangerously low on our backup server, and we suspect that a few unoptimized, massive files inside our backup archives are the culprits. 

In `/home/user/backups`, there are several `.zip` files. Some of these files might be corrupted (invalid zip headers), while others contain multiple files of varying uncompressed sizes. 

To manage our disk space efficiently, we need to identify which archives contain the largest uncompressed files **without actually extracting them**, as we don't have the disk space to do so.

Your task is to:
1. Write a Python script at `/home/user/find_bloat.py` that processes all `.zip` files in `/home/user/backups`.
2. For each zip file, the script must verify if it is a valid zip archive. If it is corrupted or invalid, skip it entirely.
3. For each valid zip file, determine the uncompressed size of the *single largest file* contained within it by reading the archive headers.
4. The Python script should output to standard out in the format: `/absolute/path/to/file.zip: <max_file_size_in_bytes>`
5. Using bash commands, pipe the output of your Python script through `sort` to order the results by the size in descending order (largest first).
6. Save the final sorted output to `/home/user/largest_backups.txt`.

The format of `/home/user/largest_backups.txt` must be exactly line-by-line:
`/home/user/backups/archive_name.zip: 12345`

Do not include corrupted or non-zip files in the final output.