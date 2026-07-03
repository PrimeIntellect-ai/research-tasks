You are acting as an assistant for a technical writer. We have inherited a messy archive of legacy documentation that needs to be organized, converted, and packaged for a new documentation portal.

Here is the situation:
1. There is an archive located at `/home/user/legacy_docs.tar.gz`.
2. There is a configuration file at `/home/user/doc_config.json` that maps keywords to destination categories.

Your task is to write and execute a script (in the language of your choice) to automate the following workflow:

**Phase 1: Extraction and Traversal**
Extract `/home/user/legacy_docs.tar.gz` into `/home/user/raw_docs/`. Recursively search through `/home/user/raw_docs/` for all files ending in `.md` and `.txt`.

**Phase 2: Encoding Conversion**
Some files in the archive were created on legacy Windows systems and are encoded in UTF-16LE. You must detect any UTF-16LE encoded `.txt` or `.md` files and convert their contents to standard UTF-8. 

**Phase 3: Organization based on Configuration**
Read `/home/user/doc_config.json`. It contains a JSON object mapping keywords to directory names, like this:
`{"keyword": "destination_directory"}`

For each `.md` and `.txt` file found:
1. Check if the original file's base name (case-insensitive) contains any of the keywords from the config.
2. If it matches a keyword, its destination category is the corresponding "destination_directory". If it matches multiple, use the first one that appears in the JSON keys.
3. If it matches no keywords, its destination category is `uncategorized`.
4. Copy the file into `/home/user/compiled_docs/<destination_category>/<filename>`. (Create the directories if they don't exist).

**Phase 4: Manifest Creation**
Create a JSON manifest file at `/home/user/manifest.json`. It must contain a single JSON array of objects representing every copied file, sorted alphabetically by the `new_path`. Each object must have exactly these keys:
- `original_path`: The full absolute path to the file in the extracted `raw_docs` directory.
- `new_path`: The full absolute path to the file in the `compiled_docs` directory.
- `was_converted`: A boolean (`true` or `false`) indicating if the file was converted from UTF-16LE to UTF-8.

**Phase 5: Archiving**
Finally, create a standard ZIP archive of the compiled documentation at `/home/user/final_docs.zip`. The zip archive should contain the `compiled_docs` folder and its contents at its root.

Ensure all outputs strictly follow the requested formats and paths.