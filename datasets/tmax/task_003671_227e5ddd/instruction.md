You are a performance engineer tasked with profiling a Monte Carlo molecular graph simulation to establish baseline metrics for automated scientific code regression testing.

You have been provided with a molecular graph topology in an adjacency list format at `/home/user/molecule.adjlist`.

Your objective is to write a Go program (`/home/user/profiler.go`) that simulates random walks on this graph, analyzes the statistical distribution of the walk lengths (latency/mixing time), and outputs a specific regression profile report.

### Requirements for `profiler.go`:

1. **Graph Parsing & Simulation:**
   - Parse `/home/user/molecule.adjlist`. The file contains one node per line followed by its neighbors, space-separated.
   - Perform 10,000 independent random walks starting from node `0`.
   - A walk terminates when it returns to node `0` OR when it reaches exactly 100 steps (whichever comes first). The starting position at node `0` counts as step 0. Moving to the first neighbor is step 1.
   - To ensure reproducible tests, initialize your random number generator exactly as follows: `walkRand := rand.New(rand.NewSource(42))`.
   - At each node, select the next neighbor by first **sorting the neighbor IDs numerically in ascending order**, then using `walkRand.Intn(len(neighbors))` to pick the index.

2. **Density Estimation (Empirical Mode):**
   - Calculate the empirical distribution (histogram) of the walk lengths.
   - Identify the "mode" (the most frequently occurring walk length). If there is a tie, take the smallest walk length.

3. **Bootstrap Confidence Intervals:**
   - Calculate the sample mean of the 10,000 walk lengths.
   - To establish a robust baseline for regression testing, compute the 95% Bootstrap Confidence Interval for the mean using the Percentile method.
   - Perform exactly 10,000 bootstrap resamples (each of size 10,000, drawn with replacement).
   - Initialize a separate RNG for the bootstrap sampling: `bootRand := rand.New(rand.NewSource(123))`.
   - Use `bootRand.Intn(10000)` to select indices from your original walk lengths array.
   - Sort the 10,000 bootstrap means. The 95% CI bounds are the 2.5th percentile and the 97.5th percentile (use indices 249 and 9749 on the sorted 0-indexed array).

4. **Output Report:**
   - The program must output the results to `/home/user/regression_report.json` matching this exact structure:
     ```json
     {
       "mean_walk_length": 5.1234,
       "mode_walk_length": 2,
       "bootstrap_ci_lower": 5.0123,
       "bootstrap_ci_upper": 5.2345
     }
     ```
   - All floating point numbers should be rounded to 4 decimal places.

To complete the task, write the Go code, compile it, and run it to produce the `regression_report.json` file.