You are assisting a storage administrator who needs to reclaim disk space by processing and consolidating a set of legacy application logs. 

Due to a poorly written rotation script that raced with the logging process, the logs were archived in a chaotic, nested format. You have been provided with an archive located at `/home/user/legacy_logs.tar`.

Your objective is to extract, filter, convert, and custom-compress these logs into a single optimized archive.

Perform the following steps exactly as specified:

1. **Nested Archive Extraction**: 
   The file `/home/user/legacy_logs.tar` contains several nested archives of different formats (e.g., `.tar.gz`, `.zip`). Extract all of them. Inside, you will find several `.jsonl` files (JSON Lines).

2. **Text Transformation**:
   Use standard bash tools (like `grep`, `sed`, or `awk`) to filter out all log lines where the JSON `"level"` field is exactly `"DEBUG"`. These lines are useless and waste space.

3. **Format Conversion & Custom Compression (Python)**:
   Write a Python script to process the remaining (non-DEBUG) JSONL lines.
   - Convert them into a single CSV file named `/home/user/processed_logs.csv` with the headers exactly as: `timestamp,level,message`
   - **Custom Compression**: To further save space, apply a custom Run-Length Encoding (RLE) to the `message` field ONLY. If any character repeats **3 or more times consecutively** in the message, replace the sequence with `[CHARxCOUNT]`. 
     *Example:* If the message is "Connection failed... retryingggg!", it should become "Connection failed[.x3] retrying[gx4]!".
     *Note:* The RLE should be case-sensitive. Spaces are treated as characters.

4. **Final Consolidation**:
   Sort the resulting CSV by the `timestamp` column in ascending order (keep the header at the top). Save the final sorted CSV at `/home/user/processed_logs.csv`.
   Finally, archive this single CSV file into a new gzipped tarball at `/home/user/optimized_logs.tar.gz`.

Ensure your Python script and bash commands are written to handle standard UNIX newlines. Make sure the final `.tar.gz` file contains only the `processed_logs.csv` file at its root.