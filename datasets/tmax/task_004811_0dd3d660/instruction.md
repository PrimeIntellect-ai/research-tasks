You are acting as an assistant to a bioinformatics researcher. The researcher has dumped a large amount of raw, messy dataset files into `/home/user/raw_datasets`. This directory contains deeply nested directories, raw `.txt` files, `.zip` archives, and `.tar.gz` archives.

The researcher has an old, compiled validation utility (a stripped binary) located at `/app/data_filter`. This utility reads dataset content from standard input (STDIN) and outputs either "VALID" or "INVALID" to standard output depending on whether the data matches the researcher's strict, undocumented schema.

Your task is to write and execute a Python-based pipeline that accomplishes the following:
1. Traverse `/home/user/raw_datasets` recursively.
2. Extract any `.zip` and `.tar.gz` archives you find into a temporary workspace. Note that archives might contain directories or files.
3. For every single plain text file (whether originally uncompressed or extracted from an archive), pipe its contents via STDIN into the `/app/data_filter` binary.
4. If the binary outputs "VALID\n", copy that file into a new directory: `/home/user/clean_datasets/`. The filename should remain the same as its original base name. You can assume all valid files have unique base names.
5. Create a Python HTTP server listening on `0.0.0.0` at port `9090`. 
   - A `GET /list` request must return a JSON response containing a list of the filenames of all valid datasets (e.g., `["sample1.txt", "data_A.csv"]`).
   - A `GET /data/<filename>` request must return the raw text contents of that specific valid file from `/home/user/clean_datasets/`.
   - Leave the server running in the background so it can be queried.

You may install any Python packages you need (like Flask or FastAPI) or use the standard library. Please start your server before completing the turn.