You are an engineer tasked with porting a legacy mathematical dependency analyzer, `libmathgraph`, to work efficiently within a minimal container environment. The source code for this tool has been vendored into your environment at `/app/libmathgraph-1.4.2`. 

Unfortunately, the vendored source is broken and unoptimized. Your objectives are as follows:

1. **Fix the Build System**: The `Makefile` in `/app/libmathgraph-1.4.2` is currently failing to link standard math libraries properly, and it hardcodes compiler flags that prevent optimization. Modify the `Makefile` so it correctly links the standard math library (`-lm`), uses `-O3` optimization, and successfully compiles the `mathgraph_solver` executable.

2. **Memory Safety and UB Repair**: The core graph traversal algorithm in `src/graph_solve.c` contains an undefined behavior (an off-by-one array access memory safety issue) that causes it to crash or produce garbage when processing highly connected nodes. Identify and fix this memory safety bug so the tool can reliably process large graphs without segmentation faults.

3. **Code Translation & Version Parsing**: The original package used a heavy Python script to parse runtime configurations and check version compatibility. We cannot ship Python in this minimal container. Write a new C program at `/app/libmathgraph-1.4.2/src/cli_wrapper.c` that reads a string representing a semantic version requirement from the command line (e.g., ">=1.4.0"), compares it against the hardcoded library version `1.4.2`, and if compatible, invokes the core solver logic from `graph_solve.c` on an input file passed as the second argument. Add this wrapper to the `Makefile` to output an executable named `mathgraph_cli`.

4. **Performance Target**: Ensure your modifications, especially the optimizations in the build step and the memory safety fix, are highly performant. The automated verification will test `mathgraph_cli` on a large dataset located at `/app/test_data/large_graph.mtx`. 

To complete the task, successfully compile the project using `make` in the `/app/libmathgraph-1.4.2` directory. Your final output must be an optimized, statically-linked executable at `/app/libmathgraph-1.4.2/mathgraph_cli`. Once built, write the string "READY" to `/home/user/status.txt`.