You are an AI assistant helping a data researcher organize newly arrived datasets.

The researcher has a directory `/home/user/incoming/` where dataset files are deposited. These files often come from legacy systems using different character encodings (specifically `utf-16le` and `iso-8859-1`). 

Your task is to write and execute a Python script at `/home/user/process_datasets.py` that processes all files currently in `/home/user/incoming/` and performs the following operations:

1. **Encoding Conversion & Parsing**: Read each file, determining its correct encoding (files will be either `utf-16le` or `iso-8859-1`). Extract the project identifier from the first line of the file, which always follows the format: `ProjectID: <ID>`.
2. **UTF-8 Normalization**: Write the entire content of the file, converted to `utf-8` encoding, into a new file located at `/home/user/organized/utf8/<ID>.txt`.
3. **Hard Link Management**: Create a hard link of the *original* legacy-encoded file from `/home/user/incoming/` into `/home/user/organized/archive/` with the name `<ID>_raw.bak`.
4. **Symbolic Link Management**: Create a symbolic link at `/home/user/organized/symlinks/<ID>_active` that points exactly to the absolute path of the newly created UTF-8 file (`/home/user/organized/utf8/<ID>.txt`).

**Environment constraints:**
- The required directories (`/home/user/organized/utf8/`, `/home/user/organized/archive/`, `/home/user/organized/symlinks/`) might not exist yet; your script should create them if necessary.
- You must use Python to perform this logic.
- After writing the script, execute it so the files are processed.

Ensure all links and files are created precisely as specified.