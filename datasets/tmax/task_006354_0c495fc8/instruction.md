You are an AI assistant helping a technical writer organize a large, fragmented documentation archive. The archive contains a mix of XML documentation files, JSON metadata, and custom binary asset blobs. You need to write a Python script to traverse this archive, extract specific information, process the binaries, and safely log the inventory.

The archive is located at `/home/user/doc_archive/`.

Please write and execute a Python script (save it as `/home/user/organize_docs.py`) that performs the following tasks:

1. **Recursive Traversal:** Recursively walk through the directory `/home/user/doc_archive/` and all its subdirectories.
2. **XML Parsing:** Find all files ending in `.xml`. Parse each XML file to find the text inside the `<title>` tag (assume the structure is `<doc><header><title>...</title></header>...</doc>`).
3. **JSON Parsing:** Find all files ending in `.json`. Parse each as JSON and extract the value associated with the `"author"` key.
4. **Binary Processing:** Find all files ending in `.blob`. These are binary asset files. Open each and read the first 8 bytes. 
   - If the first 8 bytes exactly match the ASCII string `DOCBLOB1`, extract the remainder of the file (everything after the 8-byte header) and save this payload to a new file in `/home/user/extracted_assets/`. 
   - The new file should be named `<original_filename_without_extension>.dat` (e.g., if the original is `image.blob`, save to `/home/user/extracted_assets/image.dat`). You must create the `/home/user/extracted_assets/` directory if it does not exist.
   - If the header does not match, ignore the file.
5. **Concurrent-Safe Logging:** As your script processes each file, it must append a single-line JSON record to a centralized log file at `/home/user/inventory.jsonl`. Because this script is designed to eventually be run by multiple concurrent worker processes, you **must** use an exclusive file lock (`fcntl.flock(fd, fcntl.LOCK_EX)`) before appending each line, and release it afterward.
   
   The JSON lines appended to `/home/user/inventory.jsonl` should strictly follow these schemas:
   - For parsed XML files: `{"file": "<absolute_path>", "type": "xml", "title": "<extracted_title>"}`
   - For parsed JSON files: `{"file": "<absolute_path>", "type": "json", "author": "<extracted_author>"}`
   - For successfully extracted blob files: `{"file": "<absolute_path>", "type": "blob", "status": "extracted"}`

Ensure your script processes all files and generates the `/home/user/inventory.jsonl` file and the extracted `.dat` files correctly. Run your script to verify it works.