As a workflow automation specialist, you need to clean and consolidate messy user data extracted from three different legacy systems. The extracted data has inconsistent character encodings, varying whitespace, mixed casing, and duplicate entries.

Your task is to write and execute a Python script (`/home/user/process_data.py`) that reads all text files in `/home/user/raw_data/`, processes them according to the rules below, and outputs the cleaned data to `/home/user/clean_unique.txt`.

Processing Rules:
1. **Character Encoding:** The directory `/home/user/raw_data/` contains three files with different encodings: UTF-8, ISO-8859-1, and UTF-16LE. Your script must read these files correctly (you can use heuristics, the `chardet` library, or try/except blocks).
2. **Normalization & Standardization:** For each line in every file:
   - Strip all leading and trailing whitespace.
   - Replace any sequence of multiple internal spaces with a single space.
   - Convert the text to lowercase.
   - Apply Unicode NFKC normalization.
   - Ignore any lines that become empty after stripping.
3. **Hash-based Deduplication:** Calculate the SHA-256 hex digest of the resulting normalized string (encoded as UTF-8). Use this hash to deduplicate the entries. If multiple lines result in the same normalized string and hash, only keep one.
4. **Output Format:** Write the deduplicated entries to `/home/user/clean_unique.txt`. 
   - Each line must be in the format: `SHA256_HASH:NORMALIZED_STRING`
   - The file must be sorted alphabetically by the `NORMALIZED_STRING`.
   - Ensure the file ends with a newline.

Your final output should be a single Python script that successfully generates the `/home/user/clean_unique.txt` file exactly as specified.