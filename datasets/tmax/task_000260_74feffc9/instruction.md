You are tasked with porting the `/usr/bin/sqlite3` binary to a "scratch" (minimal empty) container. To do this, you must gather the executable and all of its required shared libraries. However, for security reasons, you cannot use `ldd` (as it can execute code in untrusted binaries). You must build a secure dependency analyzer.

Your objectives:

1. **gRPC Service Definition**
   You have been provided a protobuf file at `/home/user/deps.proto`:
   ```protobuf
   syntax = "proto3";
   package deps;
   service DependencyAnalyzer {
       rpc Analyze (AnalyzeRequest) returns (AnalyzeResponse);
   }
   message AnalyzeRequest {
       string binary_path = 1;
   }
   message AnalyzeResponse {
       repeated string shared_libraries = 1;
   }
   ```
   Compile this protobuf file into Python code in the `/home/user/` directory.

2. **Graph Traversal & Shared Library Resolution**
   Create a Python gRPC server in `/home/user/server.py` that implements the `DependencyAnalyzer` service.
   - The `Analyze` RPC must take the absolute path of an ELF binary and return a list of absolute paths of *all* its shared library dependencies, recursively.
   - **Constraint**: You must extract direct dependencies using `readelf -d <file>` and parsing the `NEEDED` attributes (e.g., `libm.so.6`). Do not use `ldd`.
   - Implement a graph traversal algorithm (BFS or DFS) to recursively discover dependencies of dependencies.
   - To map a `NEEDED` filename to an absolute path, search in this exact order: `/lib/x86_64-linux-gnu`, `/usr/lib/x86_64-linux-gnu`, `/lib`, `/usr/lib`. If a library is not found in any of these, skip it.

3. **Property-Based Testing**
   Write a property-based test in `/home/user/test_server.py` using `hypothesis`.
   - Abstract your graph traversal logic so it can take a mock "dependency resolver" function instead of actually running `readelf`.
   - Use `hypothesis` to generate random directed graphs (e.g., a dictionary mapping a node to a list of child nodes) which may contain circular dependencies.
   - Write a test to ensure your traversal algorithm visits all reachable nodes from a given starting node exactly once, and terminates successfully without infinite loops when circular dependencies are present.

4. **Execution & Packaging**
   Write a client script `/home/user/client.py` that calls your running gRPC server with the target `/usr/bin/sqlite3`.
   - Save the absolute paths of all resolved shared libraries (plus `/usr/bin/sqlite3` itself) to `/home/user/bundle_list.txt`. The list must be sorted alphabetically, one path per line.
   - Finally, create an uncompressed tar archive at `/home/user/minimal_sqlite3.tar` containing exactly the files listed in `/home/user/bundle_list.txt`, preserving their absolute file paths.