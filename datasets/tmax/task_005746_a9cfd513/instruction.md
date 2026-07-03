You are acting as a storage administrator for a high-performance computing cluster. We are critically low on disk space in one of our main volumes. 

In the directory `/home/user/storage_dump`, there is a split archive containing old historical node metrics. The archive pieces are named `metrics_backup.tar.gz.aa`, `metrics_backup.tar.gz.ab`, etc. 

Your objectives are to extract this data, transform the messy text logs into a compact CSV, convert that CSV into a highly packed custom binary format using Rust to maximize space savings, and finally clean up all raw data.

Follow these steps exactly:

1. **Reconstruct and Extract:**
   Reconstruct the split gzip-compressed tar archive and extract its contents. You will find several `.log` files containing raw system metrics.

2. **Text Transformation (Shell):**
   The log files contain lines mixed from different nodes with a lot of verbose boilerplate. 
   Format of lines:
   `[<TIMESTAMP>] [<LOG_LEVEL>] [<NODE_ID>] - CPU: <C>% RAM: <R>MB DISK: <D>GB MSG: <MESSAGE>`
   *Example:* `[1710002000] [INFO] [NODE_77] - CPU: 45% RAM: 8192MB DISK: 500GB MSG: Health check passed`

   Using shell utilities (like `awk`, `sed`, `grep`), extract only the records for `[NODE_42]`. 
   Transform these specific lines into a strict CSV format (no header) with the columns: `timestamp,cpu,ram,disk`.
   *Example output line:* `1710002000,45,8192,500`
   Save this intermediate file wherever you like (e.g., `/home/user/temp.csv`).

3. **Format Conversion (Rust):**
   Create a new Rust project in `/home/user/metrics_converter`. 
   Write a Rust program that reads your intermediate CSV file and converts it into a custom, highly-packed binary format file named `/home/user/metrics.bin`.
   
   The binary format specification MUST be exactly as follows:
   - **Header:** The first 4 bytes must be the ASCII magic string `METR`.
   - **Records:** For each line in the CSV, append a contiguous 17-byte record consisting of:
     - `timestamp`: 64-bit unsigned integer (u64), Big-Endian
     - `cpu`: 8-bit unsigned integer (u8)
     - `ram`: 32-bit unsigned integer (u32), Big-Endian
     - `disk`: 32-bit unsigned integer (u32), Big-Endian

   Compile and run your Rust program to generate `/home/user/metrics.bin`. You may use standard library only or add crates like `csv` if you prefer, but standard library `str::split` is perfectly fine.

4. **Space Reclamation:**
   As a storage admin, your final goal is to reclaim space. 
   Delete the entire `/home/user/storage_dump` directory.
   Delete any intermediate `.csv` or `.log` files you created or extracted outside the Rust project.
   The only things remaining related to this task should be the `/home/user/metrics_converter` directory and the `/home/user/metrics.bin` file.