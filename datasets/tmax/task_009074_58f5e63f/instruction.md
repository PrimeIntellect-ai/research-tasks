I am currently working on a data processing pipeline, but the build keeps failing. I have a bash script located at `/home/user/pipeline.sh` that iterates over a set of CSV files in the `/home/user/data/` directory and passes them to a Python script, `/home/user/process.py`, which calculates the sample variance of the numbers in each file.

Currently, the pipeline is failing for two reasons:
1. The bash script is throwing errors and failing to find certain files.
2. The Python script is crashing with an `AssertionError: Negative variance detected!` on one of the datasets. I suspect there is a numerical instability issue (catastrophic cancellation) in the way the variance is currently being calculated in `process.py` when dealing with numbers that are very large but very close together.

Your task is to debug and fix both `/home/user/pipeline.sh` and `/home/user/process.py`. 

Requirements:
1. Fix `pipeline.sh` so that it correctly iterates over all CSV files in `/home/user/data/` and passes them to the Python script, even if the filenames contain spaces or special characters.
2. Ensure `pipeline.sh` appends the output of the Python script to a file named `/home/user/results.txt`.
3. Fix the mathematical implementation in `process.py` to calculate the sample variance in a numerically stable way (e.g., using Python's built-in libraries or a stable algorithm) so that it no longer produces negative variances due to floating-point errors.
4. Keep the output format of `process.py` the same (it should print `<filename>: <variance>`), but update it to round the final variance to exactly 4 decimal places before printing. Keep the assertion that ensures variance is >= 0.
5. Run your fixed `/home/user/pipeline.sh` to generate the final `/home/user/results.txt` file.

The automated tests will verify that `/home/user/results.txt` contains the correct rounded variances for all files in the data directory.