You are acting as a technical writer organizing a massive stream of live documentation. 

A background tool located at `/home/user/generate_docs.py` generates a continuous stream of raw markdown documentation to its standard output. This output simulates a live writing process that produces thousands of lines of documentation.

Your task is to capture this stream and organize it on the fly into manageable, chunked files.

Specifically, you must:
1. Create a Python script at `/home/user/chunker.py` that reads text from standard input (`sys.stdin`) in a streaming fashion.
2. The script must create the directory `/home/user/organized_docs/` if it does not already exist.
3. As it reads the stream, it must split the incoming text into chunks of exactly 500 lines each.
4. It must save each chunk into the `/home/user/organized_docs/` directory using the naming convention `section_XXX.md`, where `XXX` is a 1-indexed, zero-padded 3-digit number (e.g., `section_001.md`, `section_002.md`).
5. After the stream ends and all chunks are written, your script must extract the very first line of each created `section_XXX.md` file and merge them into a single summary file at `/home/user/organized_docs/merged_index.md` (preserving the order of the sections).

To execute the process, you must pipe the output of the generator directly into your script using the shell:
`python3 /home/user/generate_docs.py | python3 /home/user/chunker.py`

Ensure that your `chunker.py` script is robust, uses streaming I/O (does not load the entire stream into memory at once), and handles path manipulations correctly.