You are an AI assistant helping a researcher organize some custom-packed datasets.

The researcher has a proprietary dataset archive located at `/home/user/research_data.bin`. The archive is both obfuscated and packed using a custom binary format. 

Your task is to:
1. Write a C++ program at `/home/user/extractor.cpp` that reads `/home/user/research_data.bin`.
2. The entire file is obfuscated by XORing every byte with `0x5A`. Your program must first reverse this XOR operation.
3. After decrypting, the binary format of the file is as follows:
   - 4-byte signature: `RDSF` (Research Data Structure Format)
   - 4-byte unsigned integer (little-endian): Number of files `N`
   - For each of the `N` files:
     - 16 bytes: Filename (ASCII, null-padded)
     - 4-byte unsigned integer (little-endian): File size in bytes `S`
     - `S` bytes: File content
4. Your C++ program should verify the `RDSF` signature (and exit if invalid), create a directory named `/home/user/extracted/`, and extract all the embedded files into this directory.
5. Compile your C++ program using `g++` and execute it.
6. The extracted files are in JSON Lines format (`.jsonl`), containing lines like `{"id": X, "v": Y}`. Using shell built-ins or standard CLI tools (like `jq`, `awk`, `sed`, `sort`), parse all the extracted `.jsonl` files, extract the `id` and `v` fields, and merge them into a single CSV file at `/home/user/merged.csv`.
7. The `/home/user/merged.csv` file must have the header `id,v` as the first line, followed by the extracted data sorted numerically by `id`.

Ensure that you follow the exact file paths and constraints provided.