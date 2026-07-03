You are a developer debugging a failing build pipeline for a mathematical data transformation service. 

We have a local build script located at `/home/user/pipeline/build.sh`. This script simulates a containerized build environment by setting up some environment variables, running a Python data transformation script (`/home/user/pipeline/transform.py`), and then verifying the output against a verified golden dataset (`/home/user/pipeline/golden.csv`).

Currently, the build is failing. The `build.sh` script exits with a non-zero status because the generated output (`/home/user/pipeline/output.csv`) does not match the golden dataset. 

Upon initial inspection of the logs, there appear to be two separate issues:
1. **Data Truncation/Leakage:** The script processes data in batches. Similar to a goroutine leak under cancellation, the batch processor drops or incorrectly handles the final chunk of data if the total number of rows is not perfectly divisible by the batch size. 
2. **Precision Misconfiguration:** There is a mismatch in the numerical precision configured in the build environment, causing microscopic floating-point diffs in the calculated values compared to the golden dataset.

Your task is to:
1. Analyze the mathematical transformation in `transform.py` and fix the batching logic so that all rows are processed and written correctly without truncation.
2. Identify and fix the environment misconfiguration in `/home/user/pipeline/build.sh` that is causing the precision errors.
3. Run `/home/user/pipeline/build.sh` to verify your fixes. 
4. Once the build passes (the `diff` command succeeds and the script prints "BUILD SUCCESS"), write the final successfully matched output to `/home/user/pipeline/final_output.csv` (it should be identical to the golden file).

Do not change the `golden.csv` or `input.csv` files. You are only allowed to modify `build.sh` and `transform.py`.