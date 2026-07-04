I am a researcher dealing with a messy dataset export. I have a compressed archive of raw data located at `/home/user/raw_research_data.tar.gz`. 

I need you to perform the following data parsing and organization operations using only Bash and standard command-line tools:

1. Create a directory at `/home/user/extracted_data/` and extract the contents of `/home/user/raw_research_data.tar.gz` into it.
2. Search within `/home/user/extracted_data/` (including all subdirectories) for all files with the `.txt` extension that are strictly larger than **50 Kilobytes** (51,200 bytes).
3. Concatenate the contents of these found large `.txt` files into a single master file located at `/home/user/merged_large_data.txt`. **Important:** The files must be concatenated in alphabetical order based on their full absolute file paths.
4. Create a directory at `/home/user/split_data/`.
5. Split the `/home/user/merged_large_data.txt` file into smaller chunks of exactly **500 lines** each. Save these chunks inside `/home/user/split_data/` with the prefix `chunk_` and a two-letter alphabetical suffix (e.g., `chunk_aa.txt`, `chunk_ab.txt`, etc.). Ensure the output files retain the `.txt` extension.
6. Finally, create a new gzip-compressed tar archive located at `/home/user/final_backup.tar.gz` that contains the entire `/home/user/split_data/` directory.

Do not include any files smaller than 50KB or non-`.txt` files in the merged data. Ensure all paths are exact as specified.