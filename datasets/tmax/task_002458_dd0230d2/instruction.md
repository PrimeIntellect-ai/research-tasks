You are an AI assistant helping a bioinformatics researcher organize their raw dataset files. 

The researcher has downloaded several datasets that are currently in different character encodings and needs them standardized, symlinked for easy access by legacy analysis pipelines, and verified with a checksum manifest.

Here is the current system state:
- A metadata file exists at `/home/user/datasets/metadata.json`. It contains a JSON list of dataset objects. Each object specifies the `source` file path, the `original_encoding` of that file, and an `alias` name.
- The raw data files are located in `/home/user/datasets/raw/`.

Your task is to write and execute a Python script (or use shell commands) to perform the following operations:
1. Create two new directories: `/home/user/datasets/processed/` and `/home/user/datasets/aliases/`.
2. Parse the `/home/user/datasets/metadata.json` file.
3. For each dataset listed in the JSON:
   a. Read the source file using its specified `original_encoding`.
   b. Save the contents of the file as UTF-8 in the `/home/user/datasets/processed/` directory. Keep the same original filename (e.g., if the source is `raw/data1.csv`, save it as `processed/data1.csv`).
   c. Create a symbolic link in the `/home/user/datasets/aliases/` directory. The symlink should be named exactly as the `alias` from the JSON, and it must point to the newly created UTF-8 file in the `processed/` directory.
4. Generate a checksum manifest file at `/home/user/datasets/manifest.txt`. This file must contain the SHA256 checksums of the converted UTF-8 files located in the `processed/` directory. 
   - The format for each line in `manifest.txt` must be: `<sha256_hash>  <filename>` (use two spaces between the hash and the basename of the file, e.g., `a1b2c3d4...  data1.csv`).
   - Sort the lines in `manifest.txt` alphabetically by filename.

Complete the task using terminal commands and any Python scripts you need to write.