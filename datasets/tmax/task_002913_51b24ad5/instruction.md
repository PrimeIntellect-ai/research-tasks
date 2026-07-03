You are assisting a researcher who is organizing experimental datasets. The lab's measurement instruments continuously output data files, but they are in an inconvenient legacy format and encoding. 

Your task is to create an automated background processor that watches for new data and transforms it instantly.

Specifically, you must do the following:
1. Create two directories: `/home/user/raw_datasets` and `/home/user/clean_datasets`.
2. Write a script at `/home/user/auto_process.sh` (make sure it is executable). You can write the actual processing logic in Python, Perl, Bash, or any other language, but `/home/user/auto_process.sh` must be the entry point that runs the continuous file watcher.
3. The script must continuously monitor the `/home/user/raw_datasets/` directory for any newly created `.tsv` files.
4. Whenever a new `.tsv` file appears, the script must:
   - Read the file. Assume all incoming `.tsv` files are encoded in `UTF-16LE` and contain tab-separated values with a header row.
   - Convert the character encoding to `UTF-8`.
   - Convert the data format from TSV to a JSON array of objects. The keys for each JSON object must be taken from the TSV header row.
   - Save the resulting JSON data into the `/home/user/clean_datasets/` directory. The output file must have the exact same base name as the input file, but with a `.json` extension (e.g., `data1.tsv` becomes `data1.json`).
5. After creating the script, launch it in the background so it is actively running and watching the directory (e.g., `nohup /home/user/auto_process.sh &`). Leave it running when you complete your turn.

Ensure your script handles standard TSV parsing correctly and produces a valid JSON array.