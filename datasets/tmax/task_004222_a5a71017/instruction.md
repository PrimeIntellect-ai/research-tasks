You are an AI assistant helping a developer organize and clean up a disorganized C++ project. The project files are located under `/home/user/project_root`. You need to perform log parsing, text editing, configuration updates, and write a C++ program to generate a final manifest.

Here are your instructions:

**Phase 1: Log Parsing and Filtering**
A recent nightly build failed. The multi-line compiler output is saved at `/home/user/project_root/logs/build.log`.
Parse this log to identify the filenames of all `.cpp` files that produced an `error:` (fatal or otherwise). 

**Phase 2: Configuration Update**
The project components are tracked in a JSON configuration file located at `/home/user/project_root/config/registry.json`. 
This file contains a `"components"` object mapping component names to their `.cpp` filenames.
Using your findings from Phase 1, modify `/home/user/project_root/config/registry.json` to remove the entries for any components whose files produced an error in the build log. Leave the rest of the JSON structure intact.

**Phase 3: Large-Scale Text Editing**
The legal team requires a license header update. Find all `.cpp` files anywhere inside `/home/user/project_root/src/` (and its subdirectories) that contain the exact string `/* TODO: UPDATE_LICENSE */`.
Modify these files in-place to replace that exact string with `/* LICENSE_UPDATED_2024 */`. 

**Phase 4: C++ Manifest Generator**
Write a C++17 program at `/home/user/workspace/build_manifest.cpp`. Your program must:
1. Include and use the single-header JSON library provided at `/home/user/libs/json.hpp`.
2. Read and parse the updated `/home/user/project_root/config/registry.json`.
3. Recursively search the `/home/user/project_root/src/` directory to find the absolute paths of the `.cpp` files for the components that remain in the JSON registry.
4. Print a CSV format to `std::cout`. The CSV must have the header `Component,Filename,AbsolutePath`.
5. The rows must be sorted alphabetically by the `Component` name.

**Phase 5: Execution and Stream Redirection**
Compile your C++ program (ensure you compile with `-std=c++17`).
Run the compiled executable and redirect its standard output to create the final manifest at `/home/user/workspace/final_manifest.csv`.

Ensure all file paths in your generated CSV are absolute. Do not use root/sudo commands.