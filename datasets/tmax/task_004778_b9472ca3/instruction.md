You are a backup administrator responsible for optimizing the storage of legacy server logs. 

We have a large nested backup archive located at `/home/user/data/daily_backup.tar`. Inside this uncompressed tarball are hundreds of `.zip` files (e.g., `server_001.zip`, `server_002.zip`). Inside each zip file are two files:
1. `info.json`: Contains structured metadata.
2. `trace.log`: Contains multi-line application logs.

Your objective is to extract only the critical data and package it into a highly compressed custom archive format using our internal tool, `fastchunker`.

**Specific Requirements:**
1. **Fix the Vendored Package**: The `fastchunker` source code is vendored at `/app/fastchunker`. However, a recent careless commit broke the package (it fails to install and import). Debug and fix the package, then install it in your environment.
2. **Filter the Logs**: For each zip file in the tar archive, read `trace.log` and extract only the error events. An error event begins with a line containing `[ERROR]` and includes all subsequent lines (like stack traces) until the next line starting with `[INFO]`, `[WARN]`, or `[ERROR]`.
3. **Extract Metadata**: Parse `info.json` to retrieve the value of the `"server_id"` field.
4. **Write the Output**: Use the fixed `fastchunker` library to write a file at `/home/user/filtered_backup.fc`. You must use the `fastchunker.ChunkWriter` class. Write a single string for each server in the format: `SERVER_ID: <server_id>\n<concatenated_error_logs>\n---`.
5. **Optimize for Speed**: A naive script that extracts files to disk before processing takes too long. You must write your optimized script at `/home/user/fast_extract.py`. Your script MUST stream the nested archives (e.g., reading zip files directly from the tar stream without writing them to disk) and process everything in memory. 

Your script `/home/user/fast_extract.py` will be tested against a baseline naive implementation. To succeed, your optimized script must achieve a **runtime speedup of at least 3.0x** compared to the baseline, and the output archive must correctly match the expected filtered data.