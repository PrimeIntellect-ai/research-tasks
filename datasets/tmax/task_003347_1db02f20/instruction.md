We are replacing a bottleneck component in our data processing pipeline. The legacy tool, located at `/app/legacy_sorter` (a stripped binary without source code), is currently used to sort large binary datasets. 

Your task is to write a high-performance C++ drop-in replacement that produces identical output but runs significantly faster by utilizing parallelization.

Here is what you need to know about the system:
1. **Data Format**: The input files contain contiguous binary records of exactly 32 bytes each, laid out as follows:
   - `uint64_t id` (8 bytes)
   - `double score` (8 bytes)
   - `char label[16]` (16 bytes, null-terminated if shorter, but otherwise 16 bytes of characters)

2. **The Oracle**: The `/app/legacy_sorter` executable takes a single argument (the path to an input binary file) and writes the sorted records to `stdout`. You must figure out the exact sorting rules (primary, secondary, etc.) by analyzing the behavior of this binary on sample data you generate.

3. **Your Objective**: 
   - Write a C++20 program that exactly replicates the sorting logic of the legacy oracle.
   - It must take the input file path as its first argument and write the sorted binary records to `stdout`.
   - Your code must be highly optimized. Standard single-threaded `std::sort` will not be fast enough. You must use multi-threading (e.g., C++17 parallel execution policies, OpenMP, or explicit threading).
   - Create a build orchestration setup from scratch using `CMake`.
   - Your build setup must correctly find and link any necessary threading libraries (e.g., TBB or OpenMP) required for parallel sorting.
   - Build your project in `/home/user/workspace`. The final compiled executable must be located at `/home/user/workspace/build/fast_sorter`.

4. **Benchmarking and Validation**:
   - During your work, you should create test files and benchmark your solution against the oracle to ensure the outputs match exactly byte-for-byte and your code is significantly faster.
   - The automated testing suite will evaluate your binary against a massive hidden dataset on a multi-core machine. Your implementation must achieve a speedup of at least **1.5x** compared to the single-threaded legacy oracle.

Set up your build, write your C++ code, and compile it. Do not leave the final executable unbuilt.