You are a performance engineer tasked with implementing and profiling a custom matrix decomposition pipeline in Bash. Your goal is to extract a matrix from an HDF5 file, compute its LU decomposition (using standard shell tools like `awk`), compare it against a reference dataset, and output a profiling report.

You have been provided with two HDF5 files (already present in the environment):
1. `/home/user/matrix.h5` - Contains a 3x3 matrix under the dataset name `/A`.
2. `/home/user/ref.h5` - Contains the reference matrices `/L` and `/U`.

Your task:
1. Write a Bash script at `/home/user/compute_lu.sh` that:
   - Uses `h5dump` to extract the 3x3 matrix `/A` from `matrix.h5`.
   - Uses `awk` (or pure Bash) to compute the LU decomposition of `A` (using the Doolittle algorithm without pivoting).
   - Extracts the reference `/L` and `/U` matrices from `ref.h5` using `h5dump`.
   - Computes the maximum absolute error (L-infinity norm of the residual) between your computed L and U matrices and the reference L and U matrices.
   - Evaluates a statistical hypothesis: if the maximum absolute error across all elements in both matrices is strictly less than `1e-5`, the test outcome is `PASS`, otherwise `FAIL`.
   - The script must be completely self-contained and run without user interaction.

2. Run and profile your script to measure its execution time. Create a final report at `/home/user/report.txt` with the exact following format:
   ```
   Execution Time: <time_in_seconds> seconds
   Max Error: <error_value>
   Test: <PASS_or_FAIL>
   ```
   *(Note: `<time_in_seconds>` should be the real/wall-clock time formatted to at least two decimal places. `<error_value>` should be your calculated maximum absolute error, e.g., `0` or `0.000000`).*

Constraints:
- You must use Bash and standard POSIX utilities (like `awk`, `sed`, `grep`, `bc`).
- You may use `h5dump` (provided by `hdf5-tools`) to read the files.
- You do not have root access. The required packages and HDF5 files are already configured in your environment.