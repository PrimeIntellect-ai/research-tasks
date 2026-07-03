You are tasked with finding and fixing a concurrency regression in a C++ data processing tool. 

A Git repository is located at `/home/user/data_processor`. 
The `main` branch (currently at `HEAD`) contains a race condition that causes the program to non-deterministically output incorrect sum values. We know that 200 commits ago (`HEAD~200`), the program was entirely stable and always output the correct result.

Your objectives:
1. Use `git bisect` (or any equivalent method) to find the exact commit hash that introduced the race condition. 
   - *Note:* During your bisection, you may encounter a range of commits where the code fails to compile due to an undeclared function. You must interpret these compiler errors and appropriately bypass or skip these commits to continue your bisection.
   - The program should be compiled using: `g++ -O3 -pthread src/processor.cpp -o proc`
   - A "good" commit will reliably output `10000000`. A "bad" commit will often output a lower number due to data races.
2. Once you have identified the first bad commit that introduced the race condition, write its full SHA-1 hash to `/home/user/bad_commit.txt`.
3. Check out the `main` branch again.
4. Fix the race condition in the code without changing the program's intended multi-threaded workload (do not reduce the number of threads or the iteration counts).
5. Save your corrected version of the source file to `/home/user/fixed_processor.cpp`.

Your final deliverables are the hash file `/home/user/bad_commit.txt` and the repaired source file `/home/user/fixed_processor.cpp`.