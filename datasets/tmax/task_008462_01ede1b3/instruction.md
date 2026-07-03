You are assisting a researcher in organizing a continuous stream of dataset entries. 

A background process writes data to a custom Write-Ahead Log (WAL) file located at `/home/user/sensor_data.wal`. Because the background process flushes data asynchronously, the WAL file sometimes contains partial or corrupted entries. 

The WAL file format is text-based and structured as follows for each entry:
1. The exact line: `---BEGIN_ENTRY---`
2. A single line containing a JSON object.
3. The exact line: `---END_ENTRY---`

Any entry that does not strictly follow this sequence (e.g., missing the END line, or containing malformed JSON) is considered corrupted and must be ignored.

Your task is to write a Python script at `/home/user/extract_data.py` that safely extracts valid entries from the WAL file and converts them into a CSV file.

Requirements for `/home/user/extract_data.py`:
1. It must open `/home/user/sensor_data.wal` and acquire an exclusive lock using `fcntl.flock` to ensure the background writer isn't interrupted mid-write.
2. It must read the contents and identify all valid JSON entries.
3. It must extract the fields `sensor_id`, `timestamp`, and `reading` from each valid JSON object.
4. It must append these records to `/home/user/clean_data.csv` in CSV format. The CSV file must include a header row `sensor_id,timestamp,reading` ONLY if the file does not already exist or is empty.
5. It must safely truncate `/home/user/sensor_data.wal` to 0 bytes after reading, before releasing the lock, so that data is not double-processed.
6. The script should be executable and run without arguments.

Once you have written the script, execute it to process the current contents of `/home/user/sensor_data.wal`.