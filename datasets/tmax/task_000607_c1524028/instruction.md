We have a directory containing server configuration files pulled from various legacy systems. Over time, configuration drift has occurred, leading to duplicated or slightly modified files. Additionally, because these files come from different OS environments, they have inconsistent character encodings.

Your task is to build a configuration management pipeline that normalizes these files, clusters them based on similarity, and extracts a stratified sample of representative configurations.

You may write your scripts in any language of your choice.

**Requirements:**

1. **Input Data**: A directory located at `/home/user/raw_configs/` contains several configuration files.
2. **Character Encoding & Cleaning**:
   - Read all files in `/home/user/raw_configs/`. You must dynamically detect or gracefully handle the fact that files may be encoded in UTF-8, UTF-16LE, or ISO-8859-1.
   - For each file, normalize the content:
     - Remove any line where the first non-whitespace character is `#` (these are comments).
     - Remove any completely empty lines.
     - Convert all remaining text to lowercase.
     - Strip leading and trailing whitespace from every remaining line.
     - Join the remaining normalized lines with a single newline character (`\n`).
3. **Similarity & Deduplication**:
   - Compute the exact Levenshtein distance between the *normalized string content* of all pairs of files.
   - Group the files into "similarity clusters". Two files are considered directly similar if their Levenshtein distance is `<= 15`. 
   - A cluster is defined as a connected component of similar files (e.g., if A is similar to B, and B is similar to C, then A, B, and C are in the same cluster).
4. **Stratified Sampling**:
   - For each cluster, select exactly one representative configuration file.
   - The representative must be the file in the cluster that has the largest **original file size in bytes** (before any normalization). 
   - In case of a tie in file size, choose the one whose filename comes first alphabetically.
5. **Logging & Monitoring**:
   - Maintain a log file at `/home/user/pipeline.log`.
   - Every time a file is successfully read and normalized, append a line: `[READ] <filename>`
   - Once clustering is complete, append a line: `[CLUSTER] Found <N> clusters` (where `<N>` is the integer number of clusters).
6. **Output**:
   - Save the final result as a JSON file at `/home/user/config_inventory.json`.
   - The JSON should have the following exact schema:
     ```json
     {
       "clusters": [
         {
           "representative": "filename.cfg",
           "members": ["filename.cfg", "other.cfg"]
         }
       ]
     }
     ```
   - Sort the `clusters` list alphabetically by the `representative` filename.
   - Sort the `members` list alphabetically within each cluster.

Please complete the setup, write your code, and generate the required `/home/user/config_inventory.json` and `/home/user/pipeline.log` files.