You are a performance engineer tasked with creating a reproducible statistical profiling pipeline to evaluate the simulated latency of two algorithm variants (Mode A and Mode B). 

Your objective is to implement the simulation in C, automate the data collection via a Bash pipeline, and perform a statistical hypothesis test using Python.

**Step 1: The C Simulator**
Write a C program at `/home/user/simulate_latency.c` that simulates the total latency of processing `N` requests. 
To ensure cross-platform reproducibility, you must use the following custom pseudo-random number generator (PRNG) exactly as written:
```c
unsigned int my_rand(unsigned int *state) {
    *state = (*state * 1103515245 + 12345) & 0x7fffffff;
    return *state;
}
```

The C program must accept exactly three command-line arguments in this order: `<mode> <seed> <N>`
- `<mode>` is either `A` or `B`.
- `<seed>` is an unsigned integer to initialize the PRNG state.
- `<N>` is the number of requests to simulate (integer).

For each request (from 1 to `N`), generate a random number using `my_rand(&state)`.
- If Mode is `A`, the latency for that request is `(rand_val % 100) / 10.0`.
- If Mode is `B`, the latency for that request is `(rand_val % 105) / 10.0`.

The program should accumulate the latency across all `N` requests and print *only* the final total latency as a floating-point number (e.g., `4952.1`) to standard output, followed by a newline.

**Step 2: The Reproducible Pipeline**
Write a Bash script at `/home/user/pipeline.sh` that does the following:
1. Compiles `/home/user/simulate_latency.c` into an executable named `/home/user/simulate_latency` (use `gcc -O3`).
2. Runs the simulation for Mode A for seeds 1 through 50 (inclusive), with `N = 1000`. Save the 50 latency totals (one per line) to `/home/user/data_A.txt`.
3. Runs the simulation for Mode B for seeds 1 through 50 (inclusive), with `N = 1000`. Save the 50 latency totals (one per line) to `/home/user/data_B.txt`.

**Step 3: Statistical Analysis Environment**
1. Create a Python virtual environment at `/home/user/venv`.
2. Install `scipy` into this virtual environment.
3. Write a Python script at `/home/user/analyze.py` that reads `/home/user/data_A.txt` and `/home/user/data_B.txt`.
4. The Python script must perform a Welch's t-test (an independent two-sample t-test that does not assume equal population variances) comparing Mode A to Mode B.
5. The script must output the results to `/home/user/stats.json` in the following exact format, with values rounded to exactly 4 decimal places:
```json
{
  "t_statistic": -12.3456,
  "p_value": 0.0001
}
```
*(Note: Use Mode A as the first sample and Mode B as the second sample in your t-test).*

Complete all of the steps above. You should leave the final generated file `/home/user/stats.json` on the disk.