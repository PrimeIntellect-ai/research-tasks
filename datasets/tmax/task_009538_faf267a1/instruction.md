I am a researcher working with an old, poorly organized experimental dataset, and I need your help to extract, filter, and process the data. 

I have a main archive located at `/home/user/research_data.zip`. Unfortunately, the data pipeline that created this archive nested several other archives inside it (combinations of `.zip` and `.tar.gz`). 

Here is what you need to do:
1. **Recursive Extraction**: Extract `/home/user/research_data.zip` into the directory `/home/user/processed/`. You must recursively extract any nested `.zip` or `.tar.gz` files you find inside until no archives remain. Delete the intermediate nested archive files after extracting them so that only the raw data directories and files remain.
2. **Directory Traversal and Metadata Search**: Once fully extracted, recursively search through `/home/user/processed/` for "trial" directories. A directory is considered a valid "trial" directory ONLY if it contains all three of these files: `metadata.xml`, `sensors.csv`, and `data.bin`.
3. **Structured Parsing & Filtering**: For each trial directory, read `metadata.xml`. It will have the following structure:
   ```xml
   <trial>
       <id>Trial_Name</id>
       <valid>true</valid>
       <binary_offset>15</binary_offset>
       <binary_length>32</binary_length>
   </trial>
   ```
   If the `<valid>` tag is `false`, ignore this trial completely. If it is `true`, proceed to process it.
4. **Data Processing**:
   * **CSV Parsing**: Read `sensors.csv` (which has headers `timestamp,value`). Calculate the arithmetic mean of the `value` column. Round this mean to exactly 2 decimal places.
   * **Binary I/O**: Read `data.bin` as a binary file. Seek to the byte offset specified by `<binary_offset>` and read exactly `<binary_length>` bytes. Compute the SHA-256 hex digest of this specific byte chunk.
5. **Report Generation**: Compile the results for all valid trials into a single JSON file at `/home/user/summary.json`. The JSON file must contain a single array of objects, sorted alphabetically by the `trial_id`. Each object must have the following format:
   ```json
   [
     {
       "trial_id": "Trial_Name",
       "average_reading": 45.67,
       "data_hash": "a1b2c3d4..."
     }
   ]
   ```

You may use any languages and standard tools available on the system (Bash, Python, etc.) to write scripts that accomplish this task. Please ensure the final output file `/home/user/summary.json` is perfectly formatted according to the specifications.