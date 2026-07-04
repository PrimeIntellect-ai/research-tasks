You are a technical writer tasked with organizing a massive dump of recovered documentation files from a legacy engineering project. The files have been extracted from a corrupted disk image into a directory tree, but they have lost their file extensions and meaningful names.

Your task is to write a Python script that organizes these files into a clean directory structure based on their binary signatures and a provided metadata registry.

Here are the details of your environment and requirements:

1. **Input Data Locations**:
   - Recovered files are scattered recursively within: `/home/user/raw_docs/`
   - A metadata registry maps file hashes to human-readable titles: `/home/user/raw_docs/metadata.json`
   - A configuration file defines how to handle different file types: `/home/user/doc_rules.ini`

2. **File Processing Rules**:
   - You must process every file in `/home/user/raw_docs/` (and its subdirectories), except for `metadata.json`.
   - Calculate the SHA-1 hash of each file to look up its `title` in `metadata.json`.
   - Read the **first 4 bytes** of each file and convert them to an uppercase hexadecimal string (e.g., `25504446`).
   - Look up this hex signature in `doc_rules.ini` to determine the target `directory` and file `extension`.

3. **Output Requirements**:
   - Create a new directory: `/home/user/organized_docs/`
   - Copy each processed file to `/home/user/organized_docs/<directory>/<title>.<extension>` (replacing `<directory>`, `<title>`, and `<extension>` with the values discovered).
   - Generate a CSV manifest at `/home/user/organized_docs/manifest.csv` with exactly the following headers: `Title,RelativePath,SHA1`
   - `RelativePath` must be the path of the file relative to `/home/user/organized_docs/` (e.g., `pdfs/System_Architecture.pdf`).
   - The CSV must be sorted alphabetically by the `Title` column.

Write and execute the Python script to complete this task. Ensure the final `manifest.csv` is correctly formatted.