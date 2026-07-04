You are helping a researcher organize and archive a set of experimental datasets. The researcher has a messy directory at `/home/user/data/` containing a mix of JSON and CSV files from different experiments.

Your task is to write a Python script (and use any shell commands necessary) to perform the following operations:

1. **Format Conversion**: Convert all `.json` files in `/home/user/data/` to `.csv` format. The JSON files contain lists of dictionaries with the keys `id` and `val`. The converted CSV files must have a header row (`id,val`) followed by the data rows.
2. **Bulk Renaming**: Standardize the names of all `.csv` files (both newly converted and existing ones). Every file in the directory has a single uppercase letter in its name representing the experiment ID (e.g., `raw_exp_A.json`, `exp_B_raw.csv`). Rename the corresponding CSV files to match the pattern `dataset_<ID>.csv` (e.g., `dataset_A.csv`, `dataset_B.csv`).
3. **Cleanup**: Delete the original `.json` files, leaving only the newly named `.csv` files in the directory.
4. **Archiving**: Create a compressed tarball archive at `/home/user/dataset_backup.tar.gz` containing only the normalized `dataset_*.csv` files. The archive should store the files such that extracting them creates a `data/` directory containing the CSVs.

Please complete these steps. The final verification will check the contents of the newly renamed CSV files and the structure of the `dataset_backup.tar.gz` archive.