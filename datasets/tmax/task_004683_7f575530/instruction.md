As a technical writer, I need your help organizing some legacy documentation provided by an external vendor. The vendor sent a nested archive, and the files inside are in an older character encoding and format. 

Here is what you need to do:

1. **Extract the nested archive:**
   I have placed an archive at `/home/user/docs_archive.zip`. This zip file contains multiple `.tar.gz` files. Extract the zip, and then extract all the nested `.tar.gz` files into a single directory named `/home/user/extracted_docs`.

2. **Fix character encodings:**
   The documentation text files (`.txt`) inside the extracted directories are currently encoded in `ISO-8859-1`. Convert all `.txt` files in `/home/user/extracted_docs` (including any subdirectories) to `UTF-8` encoding. Overwrite the original `.txt` files with the new UTF-8 content using standard stream redirection or your tool of choice.

3. **Convert metadata formats:**
   Alongside the text files, there are multiple `.csv` files containing metadata. Each CSV has no header and contains three columns: `filename`, `author`, and `date`. 
   Write a script (e.g., in Python, Node.js, or awk) to read all `.csv` files in `/home/user/extracted_docs` and combine their data into a single JSON file located at `/home/user/metadata.json`. 
   The JSON file must contain a single JSON array of objects. Each object must have the exact keys: `"file"`, `"author"`, and `"date"`.

4. **Package the final documentation:**
   Once the text files are converted to UTF-8 and the JSON metadata is generated, create a final archive at `/home/user/final_docs.tar.gz`. This archive should contain:
   - All the `.txt` files (flattened or keeping their directory structure, as long as they are present).
   - The `metadata.json` file.
   Make sure not to include any `.csv` or `.tar.gz` files in this final archive.

Please complete these steps. I will verify the contents of `/home/user/metadata.json` and `/home/user/final_docs.tar.gz` when you are done.