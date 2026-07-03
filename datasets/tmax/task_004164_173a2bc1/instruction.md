You are an engineer tasked with setting up a polyglot build orchestrator from scratch. This system needs to determine build orders, interact with a fast C-based graph solver, and ensure build scripts are safe to run.

Your multi-stage objective is as follows:

**Part 1: Vision-based Dependency Extraction**
We have a legacy architecture diagram located at `/app/architecture.png`. You need to extract the dependency graph from this image (you may use `tesseract` or other tools available). The image contains text outlining dependencies in the format `ModuleA -> ModuleB` (meaning ModuleA depends on ModuleB, so ModuleB must be built before ModuleA). Recover these relationships.

**Part 2: Core Graph Resolver (C & FFI)**
To handle large dependency graphs efficiently, the graph traversal must be implemented in C.
Write a C file at `/home/user/libgraph.c` and compile it into a shared library `/home/user/libgraph.so`.
It must expose a function to compute a valid topological build order (dependencies must be built before the modules that depend on them).
You have the freedom to design the C function signature, but it must be callable from Python via `ctypes`.

**Part 3: Build Script Sanitizer**
We cannot trust all build scripts. You must write a Python script `/home/user/sanitizer.py` that acts as a classifier to detect malicious or dangerous build steps.
We have provided two corpora of build scripts:
- An "evil" corpus at `/app/corpus/evil/` containing scripts with network exfiltration, arbitrary file deletion, or out-of-bounds writes.
- A "clean" corpus at `/app/corpus/clean/` containing safe, standard build scripts.

Your sanitizer must take a single file path as a CLI argument:
`python3 /home/user/sanitizer.py <file_path>`
It must exit with code `0` if the script is clean, and exit with code `1` if the script is malicious. It should perform static analysis on the file contents to flag unsafe commands (e.g., `curl`, `wget`, `rm -rf`, writing to `/etc` or `/`).

**Part 4: Orchestrator Integration**
Write the main orchestrator script at `/home/user/build_system.py`. This script must:
1. Incorporate the dependencies extracted from `/app/architecture.png`.
2. Map the module names to a format suitable for your C library.
3. Call your `libgraph.so` using `ctypes` to perform the topological sort.
4. Output the final valid build order (module names separated by commas, e.g., `ModuleB, ModuleA`) to `/home/user/build_order.txt`. If multiple valid topological sorts exist, any valid one is acceptable.

Ensure all files are created in `/home/user/` and have the appropriate permissions.