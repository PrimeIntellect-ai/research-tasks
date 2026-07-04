You are assisting a technical writer with recovering and organizing a set of legacy documentation assets. 

The writer has a directory of proprietary asset files located at `/home/user/legacy_docs/`. These files have an `.asset` extension and use a custom binary format. 

Here is the specification for the `.asset` file format:
- **Bytes 0-3**: A 4-byte ASCII magic number: `DOCS`
- **Bytes 4-7**: A 32-bit big-endian integer representing the Asset Type. 
  - Type `1` indicates a Text Document.
  - Type `2` indicates an Image.
- **Bytes 8-15**: An 8-byte UNIX timestamp (ignore this).
- **Bytes 16 to EOF**: The raw payload data.

Your objective is to extract and clean the text documents by performing the following steps:

1. **Header Extraction & Filtering**: Create a directory called `/home/user/extracted_docs/`. Read through all `.asset` files in `/home/user/legacy_docs/`. Identify only the files that are of Type `1` (Text Document). Extract their payload (starting from byte 16) and save it to `/home/user/extracted_docs/` using the original base filename but with a `.txt` extension (e.g., `doc_A.asset` becomes `doc_A.txt`). You must write a Python script to do this safely.

2. **Text Transformation**: The extracted text documents contain outdated template markers and editorial notes. Create a directory called `/home/user/final_docs/`. Using command-line text processing tools (like `sed` or `awk`), process each `.txt` file in `/home/user/extracted_docs/` and apply the following rules:
   - Completely remove any line that starts exactly with the string `DRAFT:` (including the newline character).
   - Replace all occurrences of the exact string `[COMPANY_NAME]` with `Acme Corp`.
   - Save the processed files into `/home/user/final_docs/` using the same filename (e.g., `doc_A.txt`).

Please complete the end-to-end task. The final state of the system will be evaluated based on the exact presence and contents of the text files in `/home/user/final_docs/`.