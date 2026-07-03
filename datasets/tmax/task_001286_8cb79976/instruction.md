You are a backup administrator tasked with archiving and organizing mixed-format log files. 

In the directory `/home/user/backups/raw`, there are several daily log files in either CSV or JSON format. You need to write a Rust program that processes these files, converts them into a standard TSV (Tab-Separated Values) format, and organizes them into a structured archive.

Here are the requirements for your Rust application:
1. Parse every `.csv` and `.json` file in `/home/user/backups/raw`.
    - CSV files have the header: `id,date,event`.
    - JSON files contain an array of objects, e.g., `[{"id": 1, "date": "2024-05-01", "event": "login"}]`.
2. Convert the parsed data into TSV format. The TSV output must NOT contain a header row. Each line should just be `id\tdate\tevent`.
3. Save the TSV files into `/home/user/backups/processed/<YYYY-MM-DD>/<original_filename_without_extension>.tsv`. 
    - The date folder `YYYY-MM-DD` should correspond to the `date` field found in the records of that specific file (you may assume all records within a single file share the same date).
4. **Hard Link Management**: To save disk space, if the resulting TSV content of a file is exactly identical to another TSV file you have already processed and written, you must create a hard link to the existing TSV file instead of writing a new file.
5. **Symlink Management**: After processing all files, create a symbolic link at `/home/user/backups/latest` that points to the date directory in `/home/user/backups/processed/` that represents the chronologically newest date.

You may create a standard Cargo project in `/home/user/archive_tool` to write and run your Rust code. You can use standard crates like `csv`, `serde`, and `serde_json` if you wish. 

Once your Rust program finishes execution, the `/home/user/backups/processed` directory and the `/home/user/backups/latest` symlink must be perfectly structured according to the rules above.