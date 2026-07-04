You are a web developer building a new microservice feature. You have a set of gRPC Protocol Buffer (`.proto`) files that define your API, but the build is currently failing due to a circular import dependency. 

The protobuf files are located in `/home/user/protos/`.
Currently, the dependency graph has a cycle: `api.proto` imports `auth.proto`, `auth.proto` imports `models.proto`, and `models.proto` imports `api.proto` (because it uses the `ApiResponse` message defined in `api.proto`).

Your task consists of two parts:

Part 1: Refactoring and Breaking the Cycle
1. Identify the circular dependency. 
2. Create a new file `/home/user/protos/base.proto` and move the `ApiResponse` message definition from `api.proto` into `base.proto`. Make sure to include the `syntax = "proto3";` declaration at the top.
3. Update `models.proto` to import `base.proto` instead of `api.proto`.
4. Ensure `api.proto` imports `base.proto` (if it still references `ApiResponse`, though for this task, just ensure the import cycle is broken and all files have the correct valid imports for the messages they use). 

Part 2: Dependency Resolution Script
To prevent future build issues, you need to write a custom build tool. Create a Python script at `/home/user/toposort.py` that does the following:
1. Parses all `.proto` files in `/home/user/protos/`.
2. Extracts the dependencies from the `import "..."` statements (ignore standard library imports like `google/protobuf/...` if any exist, only consider local `.proto` files).
3. Performs a topological sort of the files to determine a valid compilation order.
4. If there are multiple valid files that can be compiled at a given step (i.e., ties in the dependency graph), break the tie by sorting their filenames alphabetically.
5. Writes the final sorted build order (just the filenames, e.g., `base.proto`, one per line) to `/home/user/build_order.log`.

Do not use any external non-standard Python libraries (like `networkx`) for the topological sort; implement the graph traversal and dependency resolution using standard Python data structures.