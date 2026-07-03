You are a developer debugging a failing bash-based build and data pipeline located at `/home/user/pipeline`. The pipeline has suffered from a simulated system crash, resulting in corrupted data, and has underlying algorithmic bugs that only recently surfaced. 

Your goal is to fix the pipeline so that running `/home/user/pipeline/build.sh` completes successfully. The build consists of three phases that you must fix:

**Phase 1: Database Journal Recovery**
The system uses a custom text-based Write-Ahead Log (WAL) located at `/home/user/pipeline/journal.dat`. Due to a crash, this file contains incomplete and corrupted transactions.
* Format: A transaction begins with `BEGIN <txid>`, contains one or more `SET <key> <value>` lines, and ends with `COMMIT <txid> <checksum>`.
* Checksum rule: The `<checksum>` must exactly equal the total number of characters in all the `<value>` strings (excluding spaces and newlines) within that transaction. 
* Task: Parse `journal.dat` and extract ONLY the `SET <key> <value>` lines from valid transactions (transactions that have a matching COMMIT and the correct checksum). Write these lines, in their original order, to `/home/user/pipeline/recovered.dat`.

**Phase 2: Delta Debugging a Failing Compilation**
The directory `/home/user/pipeline/src/` contains 500 source files (`*.src`). One of these files has a syntax error that causes the compiler script `/home/user/pipeline/compile.sh` to fail.
* `compile.sh` accepts a list of files as arguments. If the poisoned file is in the list, it exits with code 1. Otherwise, it exits with code 0.
* Task: Write a bash script using Delta Debugging (bisection) to efficiently identify the single poisoned file. 
* Once identified, write the exact filename (e.g., `file_123.src`) to `/home/user/poison.txt` and delete the file from the `src/` directory.

**Phase 3: Diagnosing Numerical Instability**
The final step of the build aggregates metrics using `/home/user/pipeline/aggregate.awk` on `/home/user/pipeline/metrics.txt`.
* Currently, `aggregate.awk` crashes with a "square root of negative number" error.
* This is due to catastrophic cancellation in the naive variance/standard deviation formula (`sqrt(sum_sq/NR - (sum/NR)^2)`) when processing large, closely-spaced numbers.
* Task: Fix `/home/user/pipeline/aggregate.awk` to compute the standard deviation in a numerically stable way (for example, by using Welford's algorithm or by shifting the mean by the first data point). Do not change the output format, only the mathematical method.

Once you have completed all three phases, run `/home/user/pipeline/build.sh`. If successful, it will generate `/home/user/pipeline/build_success.flag`. Leave this file in place for verification.