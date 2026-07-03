You are a platform engineer maintaining a CI/CD pipeline for a data analytics startup. A critical Python package, `math_accel`, which relies on a C extension, is failing its CI build steps. 

Your tasks are to fix the build system, verify the semantic version, and benchmark the result. All files are located in `/home/user/ci_pipeline`.

1. **Fix the Build System**:
   The package is located at `/home/user/ci_pipeline/math_accel`. When you try to compile it using `python3 setup.py build_ext --inplace`, it compiles but fails to import due to missing symbols (specifically, `pow` from the standard C math library). Modify `/home/user/ci_pipeline/math_accel/setup.py` to correctly link against the standard math library during the build process. Then build the extension in-place.

2. **Semantic Version Verification**:
   The CI pipeline requires ensuring the new version is strictly greater than the baseline. 
   Write a Python script at `/home/user/ci_pipeline/version_check.py` that takes exactly two positional arguments (version strings). The script must use proper semantic version comparison (ignoring build metadata but respecting pre-release tags like alpha/beta). It should write the larger of the two versions to `/home/user/ci_pipeline/version_out.txt`.
   Run your script with the arguments: `1.2.1-beta.2` and `1.2.1-beta.11`.

3. **Performance Benchmarking & Sorting**:
   There is a benchmarking script at `/home/user/ci_pipeline/benchmark.py`. Once the C extension is successfully built in-place (meaning `math_accel` can be imported from the `math_accel` directory), run `python3 /home/user/ci_pipeline/benchmark.py`.
   This will output a file named `/home/user/ci_pipeline/benchmark_results.txt` containing comma-separated lines of format: `Method,ExecutionTime_Seconds`.
   Sort this file by the execution time (the second column) in ascending numerical order, and save the sorted output to `/home/user/ci_pipeline/sorted_results.txt`. The output must preserve the exact format, just sorted.

Constraints:
- Do not use root/sudo. 
- You may install standard utilities or python packages like `packaging` if needed via pip.