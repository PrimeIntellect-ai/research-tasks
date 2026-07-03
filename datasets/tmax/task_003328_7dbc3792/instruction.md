I am migrating a legacy Python 2 data processing pipeline to Python 3. The pipeline processes several data files, but there are two main issues I need your help with:

1. **Graph Resolution & Execution:** The order in which the data files must be processed is defined in a dependency graph file located at `/home/user/migration/deps.txt`. Each line specifies a dependency (e.g., `fileB depends on fileA`). You need to write a Python 3 script `/home/user/migration/orchestrator.py` that parses this file, performs a topological sort to determine the correct execution order, and then sequentially executes the processing script on each file. 
2. **Shared Library Link Issue & Syntax:** The processing script `/home/user/migration/process.py` is currently written in Python 2 and fails in Python 3. Additionally, it relies on a C shared library (`libprocessor.so`) which needs to be compiled using the CMake project in `/home/user/migration/src`. The script currently hardcodes the library path incorrectly for the new environment, simulating a common link-time/runtime library loading failure.

Here is what you need to do:
- Update `process.py` so it is completely compatible with Python 3. Fix any Python 2 syntax errors (like old `print` statements or `xrange`).
- Compile the CMake project in `/home/user/migration/src` to generate `libprocessor.so`.
- Fix the `ctypes.CDLL` path in `process.py` so it correctly loads the newly built `libprocessor.so`.
- Write `/home/user/migration/orchestrator.py` to calculate the topological execution order from `deps.txt`, run `python3 process.py <filename>` for each file in the correct order, and concatenate all the processed outputs into a single file at `/home/user/migration/final_output.txt`.
- Diff `/home/user/migration/final_output.txt` against `/home/user/migration/expected_output.txt` and redirect the output to `/home/user/migration/diff_result.txt` (the diff should be empty if everything is correct).
- Write the determined topological sort order (comma-separated, e.g., `fileA,fileB,fileC`) to `/home/user/migration/execution_order.txt`.

Ensure all files are created exactly at the specified paths.