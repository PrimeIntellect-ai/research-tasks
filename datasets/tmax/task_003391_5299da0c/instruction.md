You are a developer tasked with organizing some project files that were received in a custom backup format.

You have been provided with a backup file at `/home/user/data/backup.json`.
This file contains a JSON object with a key `"chunks"`. The value is a list of strings.
Each string is a chunk of a tar archive that has been processed in the following way:
1. A chunk of the tar archive was zlib-compressed.
2. The compressed bytes were then Base64 encoded.

Your objective is to:
1. Read `/home/user/data/backup.json`.
2. Base64 decode and zlib decompress each chunk.
3. Concatenate the decompressed chunks in the original order to perfectly reconstruct the tar archive.
4. Extract the contents of the tar archive into the directory `/home/user/project/`.
   - **CRITICAL SECURITY REQUIREMENT:** The archive is known to contain a "Zip Slip" directory traversal attack (files with paths like `../` or absolute paths that would extract outside the target directory).
   - You MUST write your extraction logic to explicitly detect and skip any files that would be extracted outside of `/home/user/project/`. Do not extract these malicious files anywhere.
5. Create a text file at `/home/user/extracted_files.txt` containing the absolute paths of all files that were successfully and safely extracted, with one path per line, sorted alphabetically.

Ensure your Python script handles the extraction securely without failing the entire process due to the malicious paths.