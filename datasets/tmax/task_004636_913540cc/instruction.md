You are an artifact manager tasked with curating a legacy binary repository. 

I have a large binary archive located at `/home/user/artifacts.bin`. Deep within this binary file, there is a specific metadata block containing a list of artifact packages. 

Your task is to extract and clean this metadata using bash built-ins and standard CLI tools.

Here are the exact specifications:
1. The metadata block starts at exactly byte offset `4096` in the file `/home/user/artifacts.bin`.
2. The metadata block is exactly `512` bytes long.
3. The text within this block is encoded in `UTF-16LE`.
4. Extract this block, convert it from `UTF-16LE` to `UTF-8`.
5. Remove any null characters (`\0`) that may have been used for padding.
6. The resulting text will be a list of artifacts, one per line. Filter out any lines that contain the exact uppercase words "OBSOLETE" or "REJECTED".
7. Sort the remaining valid artifact names alphabetically.
8. Save the final curated list to `/home/user/curated_list.txt`.

Ensure your final file contains only the clean, valid artifact names, one per line.