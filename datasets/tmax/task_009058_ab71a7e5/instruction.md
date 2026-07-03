You have recently joined a team and inherited an unfamiliar C++ codebase. There is a simple utility program at `/home/user/concurrent_processor.cpp` that is supposed to calculate the sum of an array of `N` ones (where `N` is provided as a command-line argument). It attempts to speed up the process by splitting the work across 4 threads.

However, the team has reported that the program is flaky. Sometimes it outputs a number slightly less than `N`. You suspect a race condition.

Your task is to:
1. Write a bash script at `/home/user/fuzz.sh` that repeatedly runs `/home/user/processor` with a random integer argument between 10000 and 50000. The script should compare the program's output to the expected output (which should be exactly the input argument). It should stop and exit with code 1 if a mismatch is found, or exit with code 0 after 50 successful runs. Make sure it is executable.
2. Compile the initial buggy code to `/home/user/processor`.
3. Run your fuzzer or use tools like ThreadSanitizer to trace and identify the exact location of the concurrency bug.
4. Fix the race condition in `/home/user/concurrent_processor.cpp`. You must keep the multithreading logic but make the state update thread-safe without drastically changing the algorithm's structure (e.g., use `std::atomic`).
5. Compile your fixed code to `/home/user/processor_fixed` (use `g++ -pthread -O2`).
6. Run `/home/user/processor_fixed 500000` and save the exact standard output to `/home/user/final_result.txt`.

Ensure all requested files are exactly in `/home/user/`.