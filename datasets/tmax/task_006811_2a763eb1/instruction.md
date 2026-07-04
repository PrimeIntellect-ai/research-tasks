You are an ML engineer preparing training data for a new model. The data comes from a legacy physics simulation written in C that outputs an HDF5 file. However, your team has noticed that the simulation produces non-reproducible results when run multiple times, which makes training unstable. The issue stems from a floating-point reduction order in the OpenMP parallel loops of the simulation.

Your task is to build a reproducible data pipeline strictly using Bash and standard Linux command-line tools (like `awk`, `grep`, `h5dump`). 

You need to write a master script at `/home/user/pipeline.sh` that does the following when executed:

1. **Compilation**: Navigate to `/home/user/sim_src` and compile the simulation using the provided `Makefile`.
2. **Reproducible Generation**: Run the resulting `./simulate` executable in a way that forces OpenMP to use exactly 1 thread, ensuring the floating-point reduction order is deterministic. The simulation will generate a file named `synth_data.h5` in the current directory.
3. **Data Reshaping**: Use `h5dump` to extract the dataset located at `/features/signal` from `synth_data.h5`. Parse and reshape this output to extract purely the floating-point numbers into a single-column, flat list (ignoring indices, brackets, and metadata).
4. **Bootstrap Confidence Interval**: Implement a bootstrap confidence interval calculation for the mean of these values directly in your Bash pipeline using `awk`.
   - Perform exactly `B=100` bootstrap resamples.
   - Sample with replacement. 
   - To guarantee exact verification, your `awk` command must initialize its random number generator with `srand(1234)` in the `BEGIN` block and use `int(rand() * N) + 1` for sampling indices.
   - Calculate the mean for each of the 100 resamples.
   - Sort these 100 means in ascending order.
   - Extract the 5th value (lower bound) and the 96th value (upper bound) to form a 90% confidence interval.
5. **Formatting**: Your `/home/user/pipeline.sh` must write the final confidence interval to `/home/user/ci_output.txt` in exactly this format (rounded to 4 decimal places):
   `CI: [Lower, Upper]`
   *(Example: CI: [12.3456, 12.7890])*

Ensure `/home/user/pipeline.sh` is executable and self-contained. Do not use Python or R; you must rely on Bash, OpenMP environment variables, `h5dump`, and `awk`/`sed`/`sort`/`tr` etc.