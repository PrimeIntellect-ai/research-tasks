You are an AI assistant helping a developer organize and consolidate legacy project files safely. 

You have been given access to a legacy data directory at `/home/user/legacy_app`. Inside this directory, there is a configuration file named `/home/user/legacy_app/config.ini`. 

Your task is to perform a data consolidation operation following these precise steps:

1. **Configuration Interpretation**: Read `/home/user/legacy_app/config.ini`. It contains an `[Export]` section specifying `input_dir`, `output_file`, `target_encoding`, `format`, and `lock_path`.
2. **File Locking**: Before beginning the data extraction, you must create the lock file specified by `lock_path` in the configuration to simulate a safe concurrent access lock.
3. **Encoding & Format Conversion**: 
   - Navigate to the `input_dir`. There are several text files inside it. These files are encoded in various character sets (e.g., ISO-8859-1, UTF-16LE).
   - You must automatically detect the encoding of each file, read its contents, and convert it to the `target_encoding` specified in the config.
   - The input files contain data in a multiline key-value format (e.g., `Item: [Name]\nPrice: [Value]\n`).
   - You must convert this data into the requested `format` (CSV) with the exact headers `Item,Price`.
4. **Output Generation**: 
   - Write the consolidated CSV data into the `output_file` specified in the config. 
   - Sort the rows alphabetically by the `Item` column.
   - The final CSV file must be exactly in the `target_encoding`.
5. **Cleanup & Verification**:
   - Delete the lock file once the output file is successfully written.
   - Create a log file at `/home/user/legacy_app/success.log` containing exactly the integer representing the total number of data records (items) successfully processed and written to the CSV.

Ensure the final CSV precisely follows this format:
```csv
Item,Price
[Item1],[Price1]
[Item2],[Price2]
```
Do not leave the lock file behind. You may use standard Linux commands, bash scripting, or write a Python script to accomplish this task.