You are tasked with debugging a failing build step for a scientific data processing pipeline. 

The pipeline consists of a precomputation script `/home/user/project/precompute.py` which is executed by `/home/user/project/build.sh`. When you run `./build.sh`, it currently fails. 

The precomputation script is supposed to:
1. Read the input file path from `/home/user/project/config.ini`.
2. Parse a series of floating-point numbers from that input file.
3. Calculate the sample variance of those numbers.
4. Write the variance to `/home/user/project/output.txt` formatted to 6 decimal places.

However, the script has several bugs:
- It exits silently with an error code before doing anything, likely due to a file I/O issue (you might want to use `strace` to see what files it is trying to open).
- The custom data parser is crashing on certain edge cases in the data file format.
- The mathematical calculation for variance suffers from floating-point precision issues (catastrophic cancellation), resulting in a wildly incorrect result for data with a large mean and small variance.

Your task:
1. Fix the file loading issue in `precompute.py`.
2. Fix the data parsing logic in `precompute.py` so it correctly extracts all floating point numbers from `/home/user/project/data.txt`.
3. Fix the variance calculation in `precompute.py` to be numerically stable (you may use standard library modules like `statistics` or implement Welford's algorithm).
4. Ensure that running `/home/user/project/build.sh` exits with code 0 and produces the correct output variance in `/home/user/project/output.txt`.

Do not modify `build.sh`, `config.ini`, or `data.txt`. Only modify `precompute.py`.