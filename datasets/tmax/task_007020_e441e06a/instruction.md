You are a performance engineer tasked with optimizing a critical legacy component.

We have an undocumented, pre-compiled binary located at `/home/user/legacy_bin`. This tool is used to process sequences of numbers, but it has a severe performance bottleneck. When run on files containing more than a few thousand numbers, it takes an unacceptable amount of time to complete. 

Your task is to:
1. **Analyze the Binary:** Figure out the algorithm `legacy_bin` is executing. It takes a single command-line argument: the path to a text file containing space-separated integers. It outputs a single metric. 
2. **Optimize:** Write a C++ program named `/home/user/optimized.cpp` that performs the exact same mathematical calculation but does so optimally (it must be able to process 1,000,000 integers in under a second). The output format must exactly match the legacy binary (e.g., `Max subarray sum: <value>\n` - oops, pretend you deduced that!).
3. **Regression Test:** Write a bash script named `/home/user/run_tests.sh` that does the following:
   - Compiles `optimized.cpp` into an executable named `/home/user/optimized_bin` (using `g++ -O3`).
   - Generates a test file `/home/user/small.txt` containing 150 random space-separated integers (including some negative numbers).
   - Runs both `legacy_bin` and `optimized_bin` on `small.txt` and asserts that their standard outputs match exactly. If they don't, the script should exit with a non-zero status.
   - Generates a large test file `/home/user/large.txt` containing 1,000,000 random integers (mix of positive and negative, ranging from -1000 to 1000).
   - Runs `optimized_bin` on `large.txt` and redirects its output to `/home/user/result.log`.

Make sure `run_tests.sh` is executable (`chmod +x`). 
You must execute your `run_tests.sh` script to produce `/home/user/result.log` before finishing the task.