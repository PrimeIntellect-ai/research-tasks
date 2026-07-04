You are assisting a technical writer who has received a disorganized documentation payload from an external vendor. The payload is packaged as a nested archive at `/home/user/vendor_docs.tar.gz`. To prevent potential directory traversal issues (like zip-slip) and to standardize the formatting, you must extract and reorganize the files according to strict rules.

Please perform the following steps using Bash:

1. **Extraction & Flattening**: Extract all Markdown (`.md`) and Text (`.txt`) files from `/home/user/vendor_docs.tar.gz` and any nested archives (`.zip` or `.tar.gz`) it contains. Place all these extracted files directly into a new directory at `/home/user/extracted_docs/`. You must flatten the directory structure (ignore original paths) and ONLY extract `.md` and `.txt` files.
2. **Bulk Renaming**: Standardize all filenames in `/home/user/extracted_docs/` by converting all letters to lowercase and replacing any spaces with underscores (e.g., `API Guide.md` becomes `api_guide.md`). 
3. **Conflict Resolution**: If two files end up with the exact same standardized name, append `_1` to the one that was extracted later (or just ensure both are kept, e.g., `api_guide.md` and `api_guide_1.md`).
4. **Manifest Generation**: Generate a SHA256 checksum manifest of all the standardized files in `/home/user/extracted_docs/`. Save this manifest to `/home/user/doc_manifest.txt`. The manifest must contain lines in the standard `sha256sum` format (`<hash>  <filename>`), and the lines must be sorted alphabetically by filename.
5. **Symlinking**: Identify the largest file (by byte size) in the `/home/user/extracted_docs/` directory. Create a symbolic link at `/home/user/primary_doc.md` that points to this largest file.

Ensure all file paths and names match the requirements precisely.