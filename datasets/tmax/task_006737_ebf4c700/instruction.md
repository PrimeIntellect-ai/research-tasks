You are an AI assistant helping a release manager prepare for a new deployment. We have a new C utility that merges two sorted data files, but we need to implement it and create an end-to-end test orchestrator to verify it concurrently before we cut the release.

Please perform the following steps:

1. Create a C program at `/home/user/release_prep/merger.c`.
   - It must take exactly two arguments: the paths to two input text files.
   - Each input file contains a sorted list of integers, one per line (can be empty).
   - The program should merge the two sorted files and print the resulting sorted sequence of integers to `stdout`, one per line.
   - You can assume valid integer inputs and that the input files fit in memory.
   - Compile it to an executable named `/home/user/release_prep/merger` using `gcc`.

2. Create a Go test orchestrator at `/home/user/release_prep/test.go`.
   - The Go program must concurrently test the `merger` executable against three datasets using Goroutines and channels or `sync.WaitGroup`.
   - The datasets are located in `/home/user/release_prep/data/`:
     - Test 1: `a1.txt` and `b1.txt` -> compare stdout to `exp1.txt`
     - Test 2: `a2.txt` and `b2.txt` -> compare stdout to `exp2.txt`
     - Test 3: `a3.txt` and `b3.txt` -> compare stdout to `exp3.txt`
   - The orchestrator should spawn a goroutine for each test case, execute the `./merger` command, capture `stdout`, and diff/compare it to the content of the corresponding `exp` file.
   - If all three tests pass (exact string match with expected output), the Go program must write the exact string `ALL PASS` to `/home/user/release_prep/status.txt`.

3. Run your Go orchestrator to perform the tests and generate the `status.txt` file.

Make sure your C code handles empty files properly, and your Go code correctly implements concurrency to run the tests in parallel.