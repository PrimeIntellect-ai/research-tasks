You are a script developer responsible for maintaining a set of mathematical data processing utilities. One of your utilities, `math_util.cpp`, processes a dataset of 3D vectors. 

The utility is supposed to:
1. Read a Base64-encoded file containing a raw array of `Point` structs (encoded as binary data).
   `struct Point { int32_t id; float x; float y; float z; float distance; };`
2. Decode the Base64 data back into memory.
3. Calculate the Euclidean distance from the origin (0,0,0) for each point and store it in the `distance` field.
4. Sort the points by distance in ascending order.
5. Output the sorted points to a CSV file in the format: `id,distance`.

However, the current C++ code in `/home/user/math_util.cpp` is failing. It crashes randomly, fails to sort correctly, and has memory leaks. It suffers from Undefined Behavior (UB), a memory management error, and an invalid sorting comparator.

Your tasks are:
1. Fix the bugs in `/home/user/math_util.cpp`. Ensure there are no memory leaks, no buffer overflows, and no undefined behavior (pay close attention to the sorting comparator and memory allocation/deallocation).
2. Compile the fixed code: `g++ -O2 -std=c++17 /home/user/math_util.cpp -o /home/user/math_util`
3. Run the compiled utility on the provided dataset: `/home/user/math_util /home/user/data.b64 /home/user/output.csv`
4. The output must be sorted by distance. There is a reference file `/home/user/expected.csv`. Generate a unified diff between the expected reference and your output, and save it to `/home/user/diff_result.txt`:
   `diff -u /home/user/expected.csv /home/user/output.csv > /home/user/diff_result.txt` (If your output is perfectly correct, the file will be empty, which is the desired outcome).

Ensure your final C++ code compiles without warnings, executes cleanly (you can verify with `valgrind` if you wish), and produces the exact expected CSV output.