I am a researcher trying to organize a batch of legacy dataset files I received from international partners. The data is currently messy, using different file formats and character encodings. I need you to normalize this data, create a manifest, and package it into a compressed archive.

Here is the current state of my files located in `/home/user/raw_data/`:
1. `dataset_alpha.csv`: A semicolon-separated CSV file. It is encoded in `ISO-8859-1`. 
2. `dataset_beta.json`: A JSON file containing a single array of objects. It is encoded in `UTF-16LE`.

Please perform the following operations:
1. **Format and Encoding Conversion:** 
   Write and execute a Python script to read both datasets and convert them into standard JSON Lines format (`.jsonl`), where each line is a valid JSON object representing a row/item from the source datasets. 
   - The output files must be named `dataset_alpha.jsonl` and `dataset_beta.jsonl`.
   - The output files must be saved in a new directory: `/home/user/processed_data/`.
   - The output files must be strictly encoded in `UTF-8`.
   - Ensure the column names/keys remain exactly as they are in the source files. Numeric values in the CSV can remain as strings, but the JSON numbers should remain numbers.

2. **Manifest Generation:**
   Inside `/home/user/processed_data/`, create a file named `manifest.txt`. This file should contain the SHA-256 checksums of the two `.jsonl` files you just created. The format for each line must be exactly: `<sha256_hash>  <filename>` (e.g., `abcdef...  dataset_alpha.jsonl`). *Note: only use the basename of the file in the manifest, not the full path.*

3. **Archive Creation:**
   Finally, create a gzip-compressed tar archive containing the entire `processed_data` directory.
   - The archive must be saved at: `/home/user/final_dataset.tar.gz`.
   - When extracted, it should extract a directory named `processed_data` containing the `.jsonl` files and the `manifest.txt`.

Please write the Python code and necessary shell commands to complete these steps. Ensure everything is placed exactly in the directories specified.