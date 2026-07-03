You are an AI assistant helping a linguistics researcher clean and organize scattered dataset fragments from a recent field study.

The researcher has a messy directory tree located at `/home/user/dataset_raw/`. Inside this directory and its subdirectories, there are several text fragments encoded in different formats due to the use of different logging devices:
- Files with the `.iso` extension are encoded in `ISO-8859-1`.
- Files with the `.u16` extension are encoded in `UTF-16LE`.

Your task is to parse, convert, merge, and chunk this data safely using standard shell utilities.

Please perform the following steps:
1. Recursively find all `.iso` and `.u16` files in `/home/user/dataset_raw/`.
2. Process the files in strict alphabetical order of their full absolute file paths.
3. Convert the contents of each file from its original encoding (`ISO-8859-1` or `UTF-16LE`) to `UTF-8`.
4. Merge the converted standard output into a single continuous stream.
5. Split this merged stream into smaller files of exactly 100 lines each (the final file may have fewer lines).
6. The split files must be named with the prefix `clean_data_` and standard alphabetic suffixes (e.g., `clean_data_aa`, `clean_data_ab`, etc.).
7. **Important Safety/Atomic Requirement:** Do not write the chunks directly to the final destination. Instead, write the chunks into the temporary directory `/home/user/tmp_processing/`. Once the splitting is completely finished, move the generated chunks into `/home/user/dataset_clean/`.

When you have finished the operation, output the total number of files moved to `/home/user/dataset_clean/`.