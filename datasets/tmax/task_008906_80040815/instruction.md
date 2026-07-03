You are helping a developer organize project files using a hybrid Go and C++ system. The tool scans directories concurrently, filters files using a custom expression engine written in C++, and logs the results into a SQLite database.

Currently, the project is in `/home/user/project` and is incomplete. Here is what you need to do:

1. **Fix the C++ Expression Evaluator & FFI**:
   In `/home/user/project/evaluator.cpp`, there is a basic interpreter for file matching expressions (e.g., `ext == ".cpp" AND size < 5000`). 
   - Implement the missing logical `AND` and `OR` evaluation logic in the `evaluate` function.
   - Expose the `evaluate_expression(const char* expr, const char* ext, int size)` function with C linkage (`extern "C"`) so it can be called via cgo. Create a corresponding `/home/user/project/evaluator.h` header file containing the C declaration.

2. **Fix the Go Concurrency & CGO integration**:
   In `/home/user/project/main.go`, the tool walks the directory `/home/user/project/data` concurrently.
   - Import the C++ FFI using `cgo`. You will need to link the C++ code. (Hint: use `//#cgo CXXFLAGS: -std=c++17` and `//#cgo LDFLAGS: -lstdc++`).
   - Fix the worker pool logic. The `jobs` channel is being sent files, but the workers are not properly receiving them or signaling completion via the `sync.WaitGroup`.

3. **Complete the Schema Migration**:
   The Go program initializes a SQLite database at `/home/user/project/files.db`. It currently creates a `files_v1` table.
   - Add a schema migration block in `main.go` that renames `files_v1` to `files_v2`, and adds a new column `matched_rule TEXT`. 
   - Ensure the program inserts the matching file paths and the rule string into `files_v2`.

4. **Build and Run**:
   Compile the C++ code into a static library or object file, then build the Go program. 
   Run the compiled Go program. The Go program takes an expression as an argument.
   Run it with the expression: `ext == ".txt" AND size < 100`
   
   Output the list of matched file paths to `/home/user/project/matched_files.log`, one per line, sorted alphabetically.

**Initial Workspace Context**:
Assume the Go program and C++ skeletons are already provided in `/home/user/project`. You must use standard CLI tools to edit the files, compile, and run the system.