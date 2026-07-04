You are an AI assistant helping a climate researcher process a batch of incoming sensor datasets.

The researcher has received a large, multi-part archive located at `/home/user/incoming/` containing sensor readings. The archive was split into multiple chunks to bypass email attachment limits. The files are named `dataset.tar.gz.aa`, `dataset.tar.gz.ab`, etc.

Your task is to:
1. Reassemble the split multi-part archive and extract its contents. 
2. Inside the extracted archive, you will find several directories (e.g., `run_01`, `run_02`, etc.). Each directory contains a `meta.json` file and a `data.csv` file.
3. Parse the `meta.json` files to determine the data quality. You only want to keep the data from directories where the `meta.json` contains the key-value pair `"quality": "high"`.
4. Merge the `data.csv` files from these "high quality" directories into a single, unified CSV file at `/home/user/combined_high_quality.csv`.
5. The final `/home/user/combined_high_quality.csv` must have exactly one header row (which matches the headers of the original `data.csv` files).
6. The data rows (excluding the header) in the final CSV must be sorted numerically in ascending order based on the first column (`timestamp`).

Please complete this task using shell commands or a script of your choice. Output the final file exactly as specified.