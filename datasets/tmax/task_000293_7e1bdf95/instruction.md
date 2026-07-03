You are a researcher organizing a benchmarking dataset for mathematical operations, but your existing pipeline is broken and non-reproducible.

In your workspace at `/home/user/workspace/`, there is a broken script named `benchmark.py`. It evaluates the performance of a mathematical model (specifically, computing the trace of $A A^T$, where $A$ is an $N \times N$ random matrix). Currently, it suffers from several issues:
1. It is hardcoded to a single matrix size ($N=100$) and does not accept command-line arguments.
2. It does not set a random seed, making the mathematical outputs non-reproducible.
3. It tries to plot the first row of the resulting matrix using `plt.show()`, which crashes or hangs in our headless Linux terminal environment due to matplotlib backend misconfiguration.

Your task is to fix this script and build a reproducible experiment tracking pipeline around it.

**Step 1: Fix `benchmark.py`**
Modify `/home/user/workspace/benchmark.py` to:
- Use `argparse` to accept `--batch_size` (integer, sets matrix size $N$) and `--seed` (integer, sets the numpy random seed).
- Set the numpy random seed immediately before generating the $N \times N$ matrix $A$ (which should be generated using `np.random.rand(N, N)`).
- Fix the matplotlib issue by configuring it to use a headless backend (`Agg`) *before* importing pyplot. Instead of `plt.show()`, save the plot as a PNG file named `/home/user/workspace/plots/plot_{batch_size}.png`. (Create the `plots` directory if it doesn't exist).
- Measure the time taken purely for the matrix multiplication and trace calculation (`B = A @ A.T` and `val = np.trace(B)`).
- Print exactly one line to standard output: a valid JSON object containing the keys `"batch_size"`, `"seed"`, `"time"`, and `"trace"`. For example: `{"batch_size": 100, "seed": 42, "time": 0.005, "trace": 33.45}`

**Step 2: Build the Reproducible Pipeline**
Create a bash script at `/home/user/workspace/run_experiments.sh`.
This script must:
- Ensure the output directory `/home/user/results/` exists.
- Run `benchmark.py` for three different batch sizes: `100`, `200`, and `300`.
- Use the fixed seed `123` for all three runs.
- Capture the JSON output from each run and append it to an experiment tracking file at `/home/user/results/tracking.jsonl` (one JSON object per line).

Execute your pipeline to generate the plots and the `tracking.jsonl` file. Do not run as root.