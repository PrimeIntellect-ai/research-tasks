I am a researcher trying to organize a large dataset of text files that were improperly archived by a colleague. The archive contains recursive symlinks that create infinite loops, causing my standard backup and processing scripts to hang indefinitely. 

I need you to write a Bash script at `/home/user/clean_dataset.sh` that will automate the cleanup and processing of this dataset. Your script must perform the following pipeline when executed:

1. **Extraction**: Extract the archive located at `/home/user/raw_data.tar.gz` into a new directory `/home/user/extracted/`.
2. **Sanitization**: Identify and permanently delete all symlinks inside `/home/user/extracted/` to break any infinite directory loops.
3. **Merging**: Find all files with the `.dat` extension within `/home/user/extracted/` (and its subdirectories) and concatenate them into a single file at `/home/user/merged.dat`. To ensure consistency, the files must be concatenated in alphabetical order based on their full paths.
4. **Transformation**: Process `/home/user/merged.dat` to create `/home/user/cleaned.dat` by applying the following text transformations:
   - Completely remove any lines that begin with the exact strings "ERROR" or "DEBUG".
   - Convert all date strings in the format `YYYY/MM/DD` to the ISO standard `YYYY-MM-DD` (e.g., `2023/04/15` becomes `2023-04-15`).
5. **Chunking**: Split `/home/user/cleaned.dat` into multiple files of exactly 50 lines each. 
   - These files must be saved in a new directory `/home/user/chunks/`.
   - The files should be named `chunk_aa.txt`, `chunk_ab.txt`, `chunk_ac.txt`, etc.
6. **Archiving**: Create a final compressed archive at `/home/user/processed_dataset.tar.gz` that contains *only* the `chunks/` directory and its contents.

Once you have written the script at `/home/user/clean_dataset.sh`, make sure it is executable and run it to verify it works correctly. Ensure all paths used in your script are absolute paths.