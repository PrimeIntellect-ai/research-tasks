You are tasked with debugging a failing build and test step for a small C++ data processing tool. 

The tool, located at `/home/user/process_queries.cpp`, is designed to read a list of queries from `/home/user/queries.txt` and compute a specific metric. However, when running the compiled program on this dataset, it crashes with a `std::out_of_range` exception.

Your objectives are:
1. **Delta Debugging**: Isolate the exact single query (which consists of an ID, an X value, and a Y value) in `/home/user/queries.txt` that triggers the crash.
2. **Formula Implementation Correction**: Inspect `/home/user/process_queries.cpp` to understand why this specific query causes the crash. The issue lies within the mathematical implementation of the `compute_hash_index` formula, which fails to handle certain inputs correctly. Fix the C++ code so that the formula always produces a valid index between `0` and `99` inclusive, preserving the original mathematical intent for positive numbers but safely wrapping negative results into the positive range (standard mathematical modulo).
3. **Verification Output**: Recompile the fixed code and run it against the single query that originally caused the failure. Create a log file at `/home/user/debug_result.txt` containing exactly one line with the ID of the failing query and its correctly computed hash index in the following format:
`ID: <query_id>, CORRECT_HASH: <hash_value>`

You can compile the code using standard `g++ /home/user/process_queries.cpp -o /home/user/process_queries`.

Do not modify the `queries.txt` file. You must use standard bash tools and basic C++ debugging to find the fault.