You are a storage administrator tasked with optimizing disk space for a collection of legacy server logs. You have been given an archive of unoptimized, messy CSV logs. Your goal is to clean them, convert them to a structured JSON format using Python, deduplicate identical files using hard links to save space, and repackage them.

Perform the following steps exactly as specified. All work should be done within `/home/user/`.

1. **Extraction**: Extract the archive `/home/user/incoming/logs.tar` into a new directory called `/home/user/staging/`.

2. **Text Transformation**: The extracted `.csv` files contain unnecessary empty lines due to a logging bug. Use command-line tools (like `sed` or `awk`) to remove all empty lines from all `.csv` files in `/home/user/staging/` in-place (or output to new files and replace the originals).

3. **Format Conversion**: Write and execute a Python script at `/home/user/convert.py` that reads every `.csv` file in `/home/user/staging/`, converts the data into a JSON array of objects (using the CSV headers as keys), and writes the output to `/home/user/json_logs/` with the exact same base filename but a `.json` extension. Make sure the JSON arrays are properly formatted.

4. **Link Management (Deduplication)**: Some logs are exact duplicates of others after cleaning. Write a script (Bash or Python) to find files in `/home/user/json_logs/` that have exactly the same content. For each set of identical files, keep one original and replace the others with a **hard link** to the original file. This ensures they share the same inode and use less disk space. 

5. **Archive Creation**: Create a new compressed archive at `/home/user/optimized_logs.tar.gz` containing the entire `/home/user/json_logs/` directory.

6. **Reporting**: Count the number of *unique* inodes among the `.json` files in `/home/user/json_logs/`. Write this single integer number to `/home/user/report.txt` using standard output redirection.

Ensure all paths and filenames match exactly what is requested.