Hello, our team is dealing with a critical issue in our log aggregation pipeline. We use a proprietary, compiled binary located at `/app/log_aggregator` to parse, transform, and sort our service logs before they are ingested into our main database. 

Recently, this binary has been crashing under heavy concurrency, leaving behind core dumps (one is provided at `/app/aggregator.core`). We cannot wait for the vendor to patch this race condition. As a DevOps engineer, you need to understand exactly how this binary transforms data and write a robust, crash-free replacement.

Your task is to:
1. Analyze the stripped binary `/app/log_aggregator` and its core dump `/app/aggregator.core`. You may want to use tools like `gdb`, `strace`, `ltrace`, or `strings` to observe its file I/O, system calls, and memory state.
2. Feed sample logs to the binary to reverse-engineer its data transformation logic (e.g., how it parses timestamps, filters specific log levels, formats the output, and sorts the timeline).
3. Implement a complete replacement script or program. You may use any programming language. 
4. Provide a wrapper script at `/home/user/solution.sh` that takes standard input and writes to standard output, matching the exact behavior of the original `/app/log_aggregator` (without crashing).

The automated verifier will pass thousands of randomly generated, unstructured log lines into both your `/home/user/solution.sh` and the original `/app/log_aggregator`. Your output must be bit-for-bit identical to the original binary's output for all inputs. Make sure your script handles standard input correctly and is executable.