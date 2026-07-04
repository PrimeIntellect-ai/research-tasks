We are performance engineers debugging a data streaming pipeline. Our primary running statistics tool has stopped working. First, a recent vendored update introduced a compilation error (a linker issue). Second, even when we bypass the build issue by using an older version, we've noticed severe floating-point precision issues under heavy load. The tool uses a naive variance calculation algorithm that suffers from catastrophic cancellation on large datasets, causing pipeline anomalies.

The broken vendored codebase is located at `/app/welford_cli`.

We have a stripped reference oracle binary at `/opt/oracle/welford_cli` that implements the mathematically stable Welford's online algorithm and produces the correct output. 

Your tasks are:
1. Diagnose and fix the compiler/linker error preventing `/app/welford_cli` from building.
2. Analyze the source code and rewrite the variance and mean accumulation logic to use Welford's online algorithm so that it matches the precision of the oracle. 
3. Ensure the output format remains exactly the same as the oracle. The tool reads `f64` floats from standard input (one per line) and prints `<count>,<mean>,<variance>` for each updated value to standard output.
4. Build the final release binary and place it exactly at `/home/user/fixed_welford_cli`.

Our automated CI test will generate thousands of random data streams, pipe them into both your binary and the oracle, and verify bit-exact identical outputs. Do not alter the I/O formatting, only fix the build and the mathematical precision.