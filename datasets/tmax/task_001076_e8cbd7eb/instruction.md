I am a researcher trying to organize some experimental datasets, but the files are messy and I need your help to clean them up and convert them into a more usable format.

I have placed an archive and its checksum in the `/home/user/dataset` directory. Here is what you need to do:

1. Verify the integrity of `/home/user/dataset/archive.zip` using the SHA-256 hash provided in `/home/user/dataset/checksum.sha256`. If the checksum is valid, extract the archive in the same directory.
2. Inside the extracted archive, you will find a configuration file named `config.ini` and several `.tsv` (tab-separated values) files containing the experimental data.
3. Write a Python script (e.g., at `/home/user/process_data.py`) and run it to perform the following operations:
   - Parse the `config.ini` file. Under the `[Headers]` section, there is a mapping of the original TSV column headers to new, cleaner column names.
   - Read all `.tsv` files extracted from the archive.
   - Convert the data from the TSV files into a single JSON Lines file (`.jsonl`). Each line should be a JSON object representing a row, but the keys must be the *new* column names defined in the `config.ini` file.
   - **Crucial:** The writing of the final output file must be **atomic** to prevent data corruption in case the script fails midway. You must write the data to a temporary file first, and then rename it to `/home/user/dataset/output.jsonl`.
   
Please complete these steps so that `/home/user/dataset/output.jsonl` contains the properly formatted JSON Lines data. Process the `.tsv` files in alphabetical order by their filename to ensure a consistent output order.