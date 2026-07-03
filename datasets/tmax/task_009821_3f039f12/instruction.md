You are an engineer setting up a custom, polyglot build system from scratch. We have a tiny interpreter for our custom build DSL written in C++, but it suffers from memory safety issues (use-after-free and memory leaks) and needs to be updated. Furthermore, we have an old build configuration file that needs to be migrated to a new schema before we can benchmark the build system.

Your objectives:

1. **Schema Migration**:
   We have an old build configuration file at `/home/user/project/build.old`. The old schema format looks like this:
   ```
   Target: <name>
   Depends: <dep1>,<dep2>,...
   Command: <bash command>
   ```
   Notice that dependencies are comma-separated. If there are no dependencies, it may just say `Depends: ` or be omitted.
   
   Our new build interpreter expects the following new schema format:
   ```
   TARGET <name>
   DEPS <dep1> <dep2> ...
   CMD <bash command>
   ```
   Notice that dependencies are now space-separated.
   Write a script to convert `/home/user/project/build.old` to the new format and save it as `/home/user/project/build.new`. Ensure you replace commas with spaces in the dependencies.

2. **C++ Memory Safety & Repair**:
   The custom build interpreter is located at `/home/user/project/minibuild.cpp`. It parses the new schema, constructs a dependency graph, and evaluates the targets using a topological sort.
   However, the code currently has a fatal memory safety bug (use-after-free) and memory management issues. 
   - Identify and fix the memory bugs in `minibuild.cpp` so that it handles memory safely.
   - Ensure there are no memory leaks or undefined behaviors when executing.

3. **Compilation & Execution (Benchmarking)**:
   - Compile your fixed `minibuild.cpp` into an executable named `/home/user/project/minibuild`. (You can use `g++ -std=c++17 -O2`).
   - Run the compiled `minibuild` passing `/home/user/project/build.new` as the first argument.
   - The interpreter will execute the commands and output a performance benchmark log to `/home/user/project/benchmark.log`.

Make sure all 3 steps are completed. The automated tests will verify that `build.new` follows the correct schema, that `benchmark.log` was successfully created, and that `minibuild` compiles and runs cleanly under memory safety tools (e.g., Valgrind) without leaks or crashes.