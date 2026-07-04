You are an AI assistant helping a technical writer organize a large, messy documentation repository. 

The writer has provided an archive of raw documentation at `/home/user/raw_docs.tar.gz`. This archive contains nested `.zip` files, which in turn contain text files representing documentation pages. The documents are currently marked with a `[DRAFT]` tag that needs to be updated.

Your task is to write a build pipeline using Bash and C to extract, map, and atomically transform these files.

Perform the following steps:

1. **Archive Extraction:**
   Unpack `/home/user/raw_docs.tar.gz` into `/home/user/extracted/`. Find all `.zip` files within the extracted contents and unzip them into `/home/user/extracted_zips/`. 

2. **Configuration Generation:**
   Using standard Bash tools, generate a configuration file at `/home/user/doc_map.conf`. 
   Each line must be in the format: `INPUT_PATH=OUTPUT_PATH`
   - `INPUT_PATH` is the absolute path to an extracted `.txt` file in `/home/user/extracted_zips/`.
   - `OUTPUT_PATH` should be `/home/user/final_docs/<filename>`, where `<filename>` is the name of the text file.

3. **Transformation via C Program:**
   Write a C program at `/home/user/transformer.c` that does the following:
   - Opens and parses `/home/user/doc_map.conf`.
   - For each file mapping, reads the input file using **memory-mapped I/O (`mmap`)**.
   - Replaces all instances of the exact string `[DRAFT]` with `[FINAL]`. (You may assume the files are small enough to fit in memory and that the replacement string is exactly the same length, simplifying the operation).
   - Writes the transformed content to a temporary file in `/home/user/final_docs/` using an atomic write strategy (i.e., write to a `.tmp` file and then use `rename()` to move it to the final `OUTPUT_PATH`). 
   
4. **Execution:**
   Compile your C program using `gcc` and run it. 

Ensure that `/home/user/final_docs/` exists before your C program runs. All final `.txt` files must exist in `/home/user/final_docs/` with `[FINAL]` instead of `[DRAFT]`, and they must have been written atomically.