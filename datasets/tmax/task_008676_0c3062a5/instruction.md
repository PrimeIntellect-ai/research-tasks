You are a technical writer tasked with recovering and organizing a set of corrupted documentation files from an old legacy system. All the recovered files have lost their original extensions and are currently saved as `.bin` files in the directory `/home/user/legacy_docs/`.

To figure out what these files are and how they should be processed, you have been provided with a CSV configuration file located at `/home/user/doc_rules.csv`.

Your task is to write a Bash script or use Bash commands to process each `.bin` file in `/home/user/legacy_docs/` according to the following rules:

1. **Header Extraction**: Extract the first 4 bytes of each file and represent them as a lowercase hexadecimal string (e.g., `25504446`).
2. **Configuration Interpretation**: Look up this 4-byte hex string in `/home/user/doc_rules.csv`. The CSV has the following columns: `MagicHex,Category,Extension,Action`.
3. **Directory Organization**: Create an output directory structure at `/home/user/organized_docs/`. Inside it, create subdirectories based on the `Category` column for each matched file.
4. **Format Conversion & Saving**:
   - Save the processed file in the corresponding Category directory.
   - The new filename must be the original filename (without the `.bin` extension) plus the correct `Extension` from the CSV (e.g., `file1.pdf`).
   - **Action `copy`**: Simply copy the original file to the new location with the new extension.
   - **Action `hex2txt`**: The file contains a 4-byte header, followed immediately by hex-encoded ASCII text. You must skip the first 4 bytes, convert the remaining hex string back into readable ASCII text, and save *only* the decoded text to the new file.

Process all files in `/home/user/legacy_docs/` and place the outputs in `/home/user/organized_docs/`. 
Ensure you strictly follow the CSV mapping for categories and extensions.