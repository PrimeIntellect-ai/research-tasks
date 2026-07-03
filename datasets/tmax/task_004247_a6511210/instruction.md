You are tasked with building a C++ configuration normalization tool to help track configuration file changes across different environments. 

In `/home/user/legacy_configs.tar.gz`, there is an archive containing several legacy configuration files in JSON and CSV formats. 
Your goal is to write a C++ program at `/home/user/config_manager.cpp` that automates the extraction, parsing, renaming, manifesting, and archiving of these configurations.

Your C++ program must perform the following pipeline:
1. **Extract**: Programmatically extract `/home/user/legacy_configs.tar.gz` into a directory named `/home/user/processing/`. (You may use system calls to `tar` for this step).
2. **Parse & Bulk Rename**: Iterate through the extracted files.
   - For `.json` files: Parse the file to find the environment and version under the JSON path `metadata.env` and `metadata.version`. (You should download and use the single-header `nlohmann/json.hpp` library for C++).
   - For `.csv` files: Read the CSV. The first row is the header. The first column is always `env` and the second column is `version`. Read the second row to get these values.
   - Rename each file in the `/home/user/processing/` directory to the format: `<env>_<version>_<original_filename>`. 
     For example, if `database.json` has env="prod" and version="v1.2", it becomes `prod_v1.2_database.json`.
3. **Manifest Generation**: Compute the SHA-256 checksum for each renamed file. Generate a file named `manifest.sha256` inside `/home/user/processing/` containing the standard output format of `sha256sum` (e.g., `<hash>  <filename>`). (You can call `sha256sum` via system calls or use an OpenSSL C++ integration).
4. **Archive Creation**: Package all the renamed config files and the `manifest.sha256` into a new archive located at `/home/user/normalized_configs.tar.gz`. The files inside the archive must not include absolute paths (i.e., they should be at the root of the archive).

Requirements:
- Ensure your code compiles with `g++ -std=c++17`.
- Run your compiled program to generate the final `/home/user/normalized_configs.tar.gz` archive.
- Do not hardcode the specific filenames from the input archive; the C++ tool must dynamically discover and process `.json` and `.csv` files in the extracted directory.