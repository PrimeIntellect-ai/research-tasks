You are a backup administrator tasked with extracting, transforming, and archiving critical log data from a legacy system. 

The source data is located in `/home/user/source_data`. This directory contains a mix of `.log`, `.txt`, and `.dat` files spread across multiple nested subdirectories.

Your objective is to:
1. Find all `.log` files within `/home/user/source_data` and its subdirectories.
2. Extract all lines from these files that contain the exact string `[CRITICAL]`.
3. Consolidate these extracted lines and sort them alphabetically (to ensure a consistent, deterministic order).
4. Since the destination storage system has strict chunking requirements, split the sorted lines into chunks of exactly 10 lines per file.
5. Save these chunked files in the directory `/home/user/archive_dest/` (create this directory if it doesn't exist). Use the prefix `chunk_` for the split files (e.g., `chunk_aa`, `chunk_ab`, `chunk_ac`).
6. Finally, generate a comma-separated manifest file at `/home/user/manifest.csv`. Every line in the manifest must contain the chunk filename and its SHA256 hash in the format: `filename,sha256hash` (e.g., `chunk_aa,d2a84f4b8b650937ec8f73cd8be2c74add5a911ba64df27458ed8229da804a26`). 
7. Sort the `manifest.csv` alphabetically by filename.

Complete this task using bash shell utilities or any programming language of your choice. Ensure that the final `manifest.csv` and the chunks in `/home/user/archive_dest/` are perfectly formatted.