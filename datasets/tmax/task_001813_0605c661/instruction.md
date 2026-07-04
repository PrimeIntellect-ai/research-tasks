You are an artifact manager tasked with curating a poorly maintained repository of binary artifacts. The repository is located at `/home/user/artifacts`.

Due to an old, faulty backup script, the directory tree contains recursive symlinks that form infinite loops. Additionally, there are many files of varying sizes, but we are only interested in large artifact "blobs."

Your task is to write and execute a Python script (`/home/user/curate.py`) that performs the following:
1. Safely traverses the `/home/user/artifacts` directory tree, explicitly avoiding infinite recursion caused by symlink loops.
2. Identifies all files with the `.blob` extension that are strictly greater than `100,000` bytes in size.
3. Opens each identified file in binary mode and reads exactly the first 32 bytes.
4. Converts these 32 bytes into a lowercase hexadecimal string.
5. Writes the results to a text file at `/home/user/curated_index.txt`.

The format of `/home/user/curated_index.txt` must be exactly as follows, with one file per line, sorted alphabetically by the absolute file path:
`/absolute/path/to/file.blob: <32-byte-hex-string>`

For example:
`/home/user/artifacts/alpha/test.blob: 89504e470d0a1a0a0000000d49484452...`

Requirements:
- You must write the solution in Python 3.
- Do not remove or modify the symlinks in the directory.
- Ensure your script completes successfully without crashing from `RecursionError` or infinite loops.
- Run your script to generate `/home/user/curated_index.txt`.