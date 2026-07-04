You are tasked with building a lightweight manifest processing tool, similar to a Kubernetes operator's pre-flight hook. We have a set of Kubernetes YAML manifests in `/home/user/manifests/`. These files contain a specific annotation `deployed-at` with timestamps in UTC.

Your requirements are:
1. **Backup Strategy:** Before making any changes, create a compressed tarball of the `/home/user/manifests/` directory and save it as `/home/user/backup/manifests.tar.gz`. You will need to create the `backup` directory.
2. **Timezone Configuration & Processing:** Write a script (in Python, Ruby, or Bash) that reads all YAML files in `/home/user/manifests/`. For each file:
   - Extract the timestamp from the `deployed-at` annotation.
   - Convert this timestamp from UTC to the `Asia/Tokyo` timezone.
   - Format the new timestamp exactly as `YYYY-MM-DD HH:MM:SS JST` (e.g., `2023-05-10 21:00:00 JST`).
   - Replace the original `deployed-at` value with this new `Asia/Tokyo` timestamp.
   - Save the modified files into a new directory: `/home/user/processed/` (keeping the original filenames).
3. **Text Processing Pipeline:** Write a Bash pipeline that uses tools like `grep`, `awk`, or `sed` to extract just the values of the `deployed-at` annotations (e.g., `"2023-05-10 21:00:00 JST"`) from all files in `/home/user/processed/`. Sort these extracted values chronologically and save the output to `/home/user/timestamps.txt`.

Ensure your scripts handle standard file paths and that the output in `/home/user/timestamps.txt` contains exactly one timestamp string per line, including the quotes if they exist in the YAML.