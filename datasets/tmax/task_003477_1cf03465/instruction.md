You are a technical writer tasked with organizing a disorganized, compressed dump of legacy documentation from various company departments. 

The raw files are provided in a compressed archive at `/home/user/raw_docs.tar.gz`. 

Your goal is to extract, clean, classify, and repackage these documents into a clean directory structure. Please perform the following steps:

1. **Extract and Traverse**: Extract `/home/user/raw_docs.tar.gz` to `/home/user/extracted_docs/`. Recursively traverse the directory structure to process the files.
2. **Text Transformation**: The company recently rebranded from "AcmeCorp" to "ZenithInc". Find all text documentation files (files ending in `.txt` or `.md`). Replace every instance of "AcmeCorp" with "ZenithInc" in these files.
3. **Binary Header Extraction**: There are several legacy binary drafts (files ending in `.bin` or `.dat`). You must use **Python** to read the first 4 bytes of each binary file. If a file's first 4 bytes exactly match the ASCII string `BDOC` (hex: `42 44 4f 43`), it is a valid legacy document. Ignore all other binary files.
4. **Reorganize**: Create a new directory at `/home/user/organized_docs/`. Inside it, create two subdirectories: `text` and `binary`. 
   - Move all processed `.txt` and `.md` files into `/home/user/organized_docs/text/`.
   - Move all *valid* binary files (those starting with `BDOC`) into `/home/user/organized_docs/binary/`.
   - Note: Flatten the directory structure when moving the files (place them directly in the `text` or `binary` folders). You can assume all original filenames are unique.
5. **Archive Creation**: Compress the entire `/home/user/organized_docs/` directory into a new archive at `/home/user/final_docs.tar.gz`.
6. **Logging**: Create a summary log file at `/home/user/processing_log.txt` with exactly the following format (replace X and Y with the integer counts):
   ```
   Text files modified: X
   Valid binary files: Y
   ```
   *Note: Only count text files that actually contained "AcmeCorp" and were modified.*

Please write and execute the necessary Python scripts and shell commands to complete this task.