You are helping a researcher organize their dataset directory. The directory contains a mix of JSON files, subdirectories, and symlinks. Because of how the data was automatically backed up, there are some symlinks that point back to parent directories, creating infinite loops.

Write a C++ program at `/home/user/data_indexer.cpp` and compile it to `/home/user/data_indexer`. 
When executed, your program must:
1. Recursively traverse the directory `/home/user/data`.
2. Safely handle symlinks by avoiding infinite loops. You must process each unique physical file exactly once (ignoring symlinks that point to already-processed files).
3. Parse every `.json` file it finds. You can use the `nlohmann/json` single-header library, which is already downloaded at `/usr/include/nlohmann/json.hpp` (you can include it via `#include <nlohmann/json.hpp>`).
4. Check if the JSON file contains a top-level key `"status"` with the string value `"ready"`.
5. If it does, extract the string value of the `"dataset_id"` key.
6. Write the results to `/home/user/index.csv`. **Crucially**, to prevent data corruption from concurrent reads by the researcher's other scripts, you must write the output to a temporary file first and then **atomically** rename/move it to `/home/user/index.csv`.

The output CSV `/home/user/index.csv` must:
- Have no header row.
- Contain rows formatted as: `dataset_id,canonical_absolute_path_to_file`
- Be sorted alphabetically by `dataset_id`.

Example output row:
`ALPHA_01,/home/user/data/subset/alpha.json`

After writing and compiling the program, run it so that `/home/user/index.csv` is generated.