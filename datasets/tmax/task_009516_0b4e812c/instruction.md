I am a technical writer organizing a large repository of legacy documentation. We recently migrated our documentation system, and I need to update our Markdown files to properly reference some proprietary binary asset files. 

All the documentation is stored in `/home/user/legacy_docs`, which contains a deep, nested directory structure. Inside this directory, there are two types of files we care about:
1. Markdown files (`.md`)
2. Binary Document Assets (`.bdoc`)

The `.bdoc` files contain embedded metadata that we need to extract. Every valid `.bdoc` file starts with a 16-byte binary header:
- **Bytes 0-3**: Magic number, exactly the ASCII string `BDOC`.
- **Bytes 4-7**: Asset ID, a 32-bit unsigned integer (little-endian).
- **Bytes 8-15**: Unix Timestamp, a 64-bit unsigned integer (little-endian).

The Markdown files contain placeholder macros that look like this: `[[ASSET_REF: filename.bdoc]]`. (Note: the macro only contains the basename of the file, not the full path).

I need you to write a C++ program (save it as `/home/user/process_docs.cpp`, compile it, and run it) that does the following:
1. Recursively traverses the `/home/user/legacy_docs` directory.
2. Finds all `.bdoc` files and parses their headers to extract the Asset ID and Timestamp.
3. Finds all `.md` files and replaces every occurrence of `[[ASSET_REF: filename.bdoc]]` with `[Asset ID: <EXTRACTED_ID>](filename.bdoc)`. 
   - For example, if `diagram.bdoc` has an Asset ID of `1042`, the text `[[ASSET_REF: diagram.bdoc]]` should become `[Asset ID: 1042](diagram.bdoc)`.
4. Generates a CSV report saved exactly at `/home/user/asset_report.csv`. The CSV must have the header `filename,AssetID,Timestamp` and list all found `.bdoc` files, sorted alphabetically by the filename (basename only).

Requirements:
- Use C++17 or later for the directory traversal (e.g., `<filesystem>`).
- Modify the `.md` files in-place (or overwrite them with the updated text).
- You are free to use standard Linux tools alongside your C++ program if needed to install dependencies, compile, or set up the environment, but the core traversal, binary extraction, and report generation must be done by your C++ code.