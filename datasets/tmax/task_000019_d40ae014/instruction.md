You are an AI assistant acting as a backup administrator. We need to consolidate and archive legacy data from different servers into a unified format before storing it long-term. 

The raw data is located in `/home/user/legacy_data/` and has two subdirectories: `win_logs/` and `csv_metrics/`.

Here is what you need to do:

1. **Process Windows Logs (`win_logs/`)**:
   - The files in `/home/user/legacy_data/win_logs/` are text files currently encoded in `UTF-16LE` and have names like `SystemLog_A1.txt`, `AppLog_B2.txt`.
   - Convert the character encoding of all these files to `UTF-8`.
   - Rename the files so they are entirely lowercase and change the extension from `.txt` to `.log` (e.g., `SystemLog_A1.txt` becomes `systemlog_a1.log`).
   - Save the processed files into a new directory: `/home/user/processed_data/logs/`.

2. **Process Metrics (`csv_metrics/`)**:
   - The files in `/home/user/legacy_data/csv_metrics/` are CSV files with headers, named like `ServerStats_Jan.csv`.
   - Convert each CSV file into a JSON file containing an array of objects (one object per row, using the CSV headers as keys).
   - Rename the files to be entirely lowercase and change the extension to `.json` (e.g., `ServerStats_Jan.csv` becomes `serverstats_jan.json`).
   - Save the processed files into a new directory: `/home/user/processed_data/metrics/`.

3. **Archive the Processed Data**:
   - Once all files are processed and placed in their respective subdirectories inside `/home/user/processed_data/`, create a compressed tarball of the `processed_data` directory.
   - The archive must be saved exactly at `/home/user/final_archive.tar.gz`.
   - The root of the archive should contain the `processed_data/` directory (e.g., extracting it should create `processed_data/logs/` and `processed_data/metrics/`).

You can use Bash, Python, or any other standard tools available in a Linux environment.