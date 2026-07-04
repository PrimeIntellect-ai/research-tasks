You are tasked with analyzing a massive configuration history dump for our infrastructure. The system outputs a continuous stream of server state configurations in a large XML file located at `/home/user/network_configs.xml`.

Because this file simulates a multi-gigabyte dump, you must process it efficiently using a streaming XML parsing approach in Python (do not load the entire XML file into memory at once).

Here are your instructions:

1. Write a Python script to stream and parse `/home/user/network_configs.xml`. The file contains a root `<dumps>` element, and many `<record>` elements. Each `<record>` contains:
   - `<timestamp>` (ISO 8601 string)
   - `<server_id>` (string)
   - `<config>` (a JSON string representing a flat dictionary of the configuration state at that moment)

2. We only care about the configuration history for the server: `core-router-01`. Ignore all other servers.

3. Track the configuration changes for `core-router-01` sequentially (ordered by timestamp, which are guaranteed to be chronological in the file). Compare the current configuration JSON dictionary against the previous one for this specific server. 
   - Note when a top-level key's value changes.
   - Note when a new key is added.
   - Note when an existing key is removed.

4. Output these changes as CSV data. The CSV should have the following columns in exactly this order: `timestamp,key,old_value,new_value`.
   - `timestamp` is the time of the change.
   - `key` is the configuration key that changed.
   - If a key was added, `old_value` must be the string `NONE`.
   - If a key was removed, `new_value` must be the string `NONE`.
   - Sort multiple key changes at the same timestamp alphabetically by the `key` name.

5. File Splitting & Chunking: To make the output manageable, you must chunk the CSV output into multiple files, each containing exactly 20 change records (the last file may have fewer). 
   - Write the chunked files to the directory `/home/user/diff_chunks/`. Create the directory if it doesn't exist.
   - Name the files `core_router_diffs_part1.csv`, `core_router_diffs_part2.csv`, etc.
   - Every chunked CSV file MUST contain the header row: `timestamp,key,old_value,new_value`.

Ensure your Python script is complete, self-contained, and generates the exact directory structure and files requested.