You are a performance engineer profiling a distributed mathematical simulation platform. One of the core analytical components—a Monte Carlo numerical integration tool used for density estimation—has been failing on near-singular input distributions due to precision issues in the current bash/awk pipeline. We need to replace it with a robust, bit-exact C implementation and wire it back into the microservice architecture.

Part 1: The C Implementation
Write a C program located at `/home/user/mc_profiler.c` and compile it to `/home/user/mc_profiler`. 
The program must read lines from `stdin` until EOF. Each line will contain two unsigned 32-bit integers separated by a space: `seed` and `iterations`.
For each line, you must perform a deterministic Monte Carlo numerical integration-like summation of the function:
`f(x) = x^3 - 2x^2 + x`

To do this, generate a sequence of random points using a Linear Congruential Generator (LCG) with the following strict rules to ensure bit-exact equivalence with our test oracle:
1. Initialize the LCG state with the given `seed` (use `uint32_t` for state).
2. For `i` from 1 to `iterations` (inclusive):
   a. Update the state: `state = (state * 1664525 + 1013904223)` (modulo 2^32, standard 32-bit unsigned overflow).
   b. Extract the sample point: `x = state % 101` (this bounds `x` to [0, 100]).
   c. Evaluate `f(x)` using 64-bit signed integer arithmetic (`int64_t`).
   d. Accumulate the result into a running total sum (initialized to 0 for each line).
3. After `iterations` steps, print the final accumulated sum (as a signed 64-bit integer) to `stdout`, followed by a newline.

Part 2: Service Composition
Our local test environment runs two services:
- A Task Emitter listening on `127.0.0.1:5001`, which streams out a set of `seed iterations` pairs when connected to.
- A Result Aggregator listening on `127.0.0.1:5002`, which expects the computed results.

You must write a bash script at `/home/user/run_pipeline.sh` that connects these services together. When executed, your script should retrieve the data stream from the Task Emitter on port 5001, pipe it through your compiled `/home/user/mc_profiler` binary, and pipe the output directly into the Result Aggregator on port 5002.

Ensure your code handles large iterations smoothly and that `/home/user/run_pipeline.sh` is executable. You do not need to start the services on ports 5001 and 5002 yourself; assume they are already running or will be started by the verification environment.