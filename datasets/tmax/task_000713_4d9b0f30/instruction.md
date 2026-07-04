You are a developer building a backend utility for a build system that needs to analyze package dependency graphs and detect circular imports. 

We have an existing proprietary utility that calculates build orders and detects cycles, but we lost its source code. We only have a stripped compiled binary located at `/app/bin/dep_solver_oracle`. 

Your task is to reverse-engineer the behavior of this binary by testing it with various inputs, and then implement a C++ replacement that perfectly matches its functionality and output format.

Here are the requirements:
1. **Schema:** The binary reads a serialized Protocol Buffer message from a file path provided as its first command-line argument. The schema is located at `/app/schema/deps.proto`. 
2. **Implementation:** 
    - You must write the core logic in C++ and expose it as a C-compatible shared library (`libdepsolver.so`) with the following signature:
      `extern "C" int solve_dependencies(const char* input_filepath, char* output_buffer, int max_buffer_size);`
    - You must also write a command-line wrapper in C++ named `dep_solver` that links against this shared library, calls the FFI function, and prints the resulting output buffer to `stdout`.
3. **Behavior:** The oracle parses the dependency graph and either outputs a deterministic build order or reports a cycle. You must deduce the exact algorithmic rules (e.g., how ties are broken in the topological sort, how cycle errors are formatted) by passing test protobuf binaries to `/app/bin/dep_solver_oracle` and observing its `stdout`.
4. **Build:** Your final executable must be compiled to `/home/user/workspace/dep_solver` and the shared library to `/home/user/workspace/libdepsolver.so`. Use a Makefile or CMake to build your project. Protobuf C++ headers and the `protoc` compiler are already installed on the system.

Create the necessary files, compile your code, and ensure `/home/user/workspace/dep_solver` produces exactly the same standard output as `/app/bin/dep_solver_oracle` for any valid protobuf input defined by `deps.proto`.