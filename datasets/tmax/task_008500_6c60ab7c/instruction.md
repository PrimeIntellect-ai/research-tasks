You are acting as a storage administrator tasked with analyzing backup nodes to reclaim wasted disk space. 

In the directory `/home/user/backups/`, you will find a configuration file named `storage_policy.ini` and several subdirectories representing storage nodes (e.g., `node_alpha`, `node_beta`, `node_gamma`).

Your task consists of the following steps:

1. **Interpret Configuration**: Read `/home/user/backups/storage_policy.ini`. It contains a `target_dirs` key under the `[Policy]` section, which lists a comma-separated set of node directories you need to analyze. You must ignore any directories not listed here.

2. **Extract Archives**: Inside each target node directory, there is an archive named `data.tar.gz`. Extract *only* the file named `usage.csv` from each of these archives. Leave the archives intact.

3. **Parse and Analyze Data using C**: 
   Write a C program (save it as `/home/user/analyzer.c` and compile it to `/home/user/analyzer`) that reads the extracted `usage.csv` files. 
   The CSV files have the following header-less format:
   `filename,filetype,size_in_bytes,last_accessed_days_ago`
   
   Your C program must calculate the total sum of `size_in_bytes` across all target CSVs for files that meet BOTH of the following criteria:
   - `last_accessed_days_ago` is strictly greater than 90.
   - `filetype` is exactly `"tmp"` or `"cache"`.

4. **Generate Manifest**: 
   Create a JSON manifest file at `/home/user/reclaim_manifest.json` containing exactly the following structure, using the total integer value calculated by your C program:
   ```json
   {
     "reclaimable_bytes": <TOTAL_BYTES_INTEGER>
   }
   ```

5. **Consolidate and Checksum**:
   Create a new gzip-compressed tar archive at `/home/user/reclaim_data.tar.gz` containing all the extracted `usage.csv` files from the target directories. The paths inside the archive should preserve the node directory structure (e.g., `node_alpha/usage.csv`).
   Finally, generate a SHA256 checksum of `/home/user/reclaim_data.tar.gz` and save the output to `/home/user/reclaim_data.sha256` (the standard output format of `sha256sum`).

Ensure all output files (`analyzer.c`, `reclaim_manifest.json`, `reclaim_data.tar.gz`, `reclaim_data.sha256`) are placed precisely in `/home/user/` as requested.