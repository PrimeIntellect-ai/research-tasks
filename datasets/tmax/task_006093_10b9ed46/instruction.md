You are tasked with building a configuration change tracking tool for a distributed system. The system receives proposed configuration changes in the form of `.conf` files. 

You need to write a C++ program and a shell script to build a multi-stage pipeline that validates, processes in parallel, and merges these configurations.

Here are the requirements:

1. **Input Data**: There is a directory `/home/user/configs` containing several configuration files (`.conf`). Each file contains key-value pairs in the format `KEY=VALUE`, one per line. The `VALUE` may contain Unicode characters (UTF-8 encoded).

2. **Validation Constraints**: 
   You must write a C++ program located at `/home/user/tracker.cpp` that reads a list of file paths provided as command-line arguments. For each file, it must validate the contents based on these rules:
   - **Key**: Must consist ONLY of uppercase ASCII letters (`A-Z`) and underscores (`_`), and be between 1 and 32 characters long.
   - **Value**: Must be between 1 and 256 bytes long. It must NOT contain any ASCII control characters (byte values 0 through 31), except for the space character (if you consider space a control char, allow it; strictly speaking space is 32, so no chars < 32). 
   - If a file contains *any* invalid line (either key or value violates the constraints, or the line doesn't have an `=`), the **entire file** must be rejected and ignored.

3. **Parallel Processing**: 
   Your C++ program must process the input files in parallel. You must use `std::thread`, `std::async`, or C++17 parallel algorithms (`std::execution::par`) to parse and validate multiple files concurrently.

4. **Merging**: 
   For all valid files, gather the key-value pairs. If multiple valid files define the same `KEY`, the value from the file whose **basename** is alphabetically highest (e.g., `z_update.conf` overrides `a_init.conf`) must be kept.

5. **Output**: 
   The C++ program should output the final merged valid keys and values to a file named `/home/user/valid_changes.tsv`. The format must be exactly:
   `KEY\tVALUE\tFILENAME`
   where `FILENAME` is the basename of the file that provided the final value.
   The output lines must be sorted alphabetically by `KEY`.

6. **Pipeline Orchestration**:
   Create a shell script `/home/user/run_pipeline.sh` that:
   - Compiles `/home/user/tracker.cpp` (using `g++ -std=c++17 -pthread -O2`).
   - Finds all `.conf` files in `/home/user/configs` and passes them as arguments to the compiled executable.
   - Ensures the executable runs and generates `/home/user/valid_changes.tsv`.

Ensure your pipeline works completely by running `bash /home/user/run_pipeline.sh`.