I am a researcher organizing my raw data files, and I need help extracting only the actual datasets, verifying their integrity, and packaging them up. 

My raw data is currently in `/home/user/datasets_raw`. It contains a messy mix of dataset files (which end in `.csv` or `.json`) along with various junk files like `.log`, `.tmp`, and `.py` scripts spread across multiple subdirectories.

I need you to write a Python script (and use any shell commands necessary) to do the following:
1. Recursively find all dataset files (`.csv` and `.json`) within `/home/user/datasets_raw`.
2. Calculate the SHA-256 checksum for each dataset file.
3. Generate a JSON manifest file at `/home/user/dataset_manifest.json`. The JSON should be a single dictionary where the keys are the relative file paths (relative to `/home/user/datasets_raw`, e.g., `experiment_1/data.csv`) and the values are their corresponding SHA-256 checksum strings.
4. Create a compressed tarball archive at `/home/user/clean_datasets.tar.gz`. This archive must contain:
   - All the `.csv` and `.json` files found, maintaining their directory structure relative to `/home/user/datasets_raw`. Do NOT include the `datasets_raw` parent directory itself in the archive paths.
   - The `dataset_manifest.json` file at the root of the archive.
   - NO junk files (`.log`, `.tmp`, etc.).

Please complete these steps. The automated verification will extract your tarball, read the manifest, and verify that the hashes match the extracted files perfectly.