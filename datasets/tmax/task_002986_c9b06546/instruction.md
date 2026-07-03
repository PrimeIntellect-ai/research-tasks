You are managing a collection of configuration exports from various legacy systems. You need to extract, validate, deduplicate, and hash specific configuration blocks from these files.

Your task is to create a processing pipeline (you may write a script in Bash, Python, or standard Unix tools) that performs the following steps. Save your final execution script as `/home/user/process.sh` and run it to produce the final output file.

1. **Input Data**: A directory `/home/user/configs/` contains several exported configuration files. 
2. **Character Encoding**: Files ending in `.utf16.txt` are encoded in UTF-16LE. Files ending in `.utf8.txt` are encoded in UTF-8. Your pipeline must handle these encodings and normalize the text to UTF-8 before processing.
3. **Extraction & Validation**: 
   - Each file contains multiple configuration entries separated by a line containing exactly `---`.
   - A valid entry MUST contain the exact line `STATE: ACTIVE`. Entries without this line must be ignored.
   - For valid entries, extract the multi-line payload located between the lines `<PAYLOAD>` and `</PAYLOAD>`. Note that these payloads contain embedded newlines.
4. **Hash-Based Deduplication**: Compute the MD5 hash of each extracted payload (exactly as it appears between the tags, including its internal newlines). Deduplicate the payloads based on this hash.
5. **Parallel Processing**: Your script should be designed to process the input files in parallel (e.g., using `xargs -P`, `parallel`, or Python's `multiprocessing`) to simulate handling a massive dataset.
6. **Output**: Write the unique MD5 hashes of the valid payloads, one per line, sorted alphabetically, to `/home/user/unique_hashes.txt`.

Ensure your script `/home/user/process.sh` is executable and run it to generate `/home/user/unique_hashes.txt`.