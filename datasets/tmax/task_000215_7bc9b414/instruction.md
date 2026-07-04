You are a platform engineer maintaining our CI/CD pipelines. Our custom C++ build graph analyzer (`/home/user/build_analyzer`) is failing in the pipeline. It parses dependency graphs, calculates a priority score for each module, and serves this data via a REST API. 

However, a recent Go-style circular import in our monorepo broke it, revealing several issues you need to fix:

1. **Information Extraction**: The original specification for the priority score calculation was lost, but a screenshot of the design doc remains at `/app/design_spec.png`. Extract the text from this image to find the exact formula for the priority score, and implement this numerical algorithm in `src/scoring.cpp`.
2. **Memory Debugging & Fixes**: The current analyzer enters an infinite loop and heavily leaks memory when encountering a circular dependency (like `A -> B -> A`). Fix the cycle detection logic in `src/graph.cpp` to correctly identify cycles and break out safely without leaking memory. Use memory profiling tools (like Valgrind or ASAN) to ensure it is clean.
3. **Cross-Compilation Build**: Update the `CMakeLists.txt` to support a conditional build flag `-DTARGET_ARCH=aarch64`. When this flag is provided, it should cross-compile using the `aarch64-linux-gnu-g++` compiler.
4. **REST API**: Complete the REST API in `src/api.cpp` using the provided `cpp-httplib` header. It must expose a `POST /analyze` endpoint that accepts a plain-text list of edges (e.g., `A->B, B->C`) and returns a JSON response with the calculated priority scores and a boolean indicating if a cycle was found.
5. **Behavioral Equivalence**: Compile your final fixed CLI binary to `/home/user/build_analyzer/build/analyzer_cli`. It must accept a single string argument of comma-separated edges, and output exactly the same text format as the reference oracle binary.

Ensure your code handles arbitrary ASCII edge lists properly. Leave the fixed API server running in the background on port `8080` when you are done.