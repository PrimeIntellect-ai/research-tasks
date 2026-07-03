You are an operations engineer triaging a broken data processing pipeline.

The pipeline uses a custom Python C-extension to perform fast risk calculations. However, the system recently underwent an OS migration, and the setup is currently broken.

Your tasks:
1. **Fix the Compilation Error:** The extension's build script is located at `/home/user/setup.py`. When you try to compile it using `python3 setup.py build_ext --inplace`, it fails to link properly due to a missing standard library. Diagnose the linker error and fix `/home/user/setup.py` so that it successfully compiles the `fast_math` module.
2. **Isolate the Numerical Instability:** Once compiled, you will use `/home/user/process_data.py`. This script reads `/home/user/data.csv` (which contains 1,000 rows of floating-point pairs). The script takes a start index and an end index as command-line arguments (e.g., `python3 process_data.py 0 1000`). Currently, running it on the entire dataset crashes with a `ValueError: Numerical instability detected in batch!` due to a catastrophic cancellation/domain error resulting in `NaN`.
3. **Delta Debugging:** Use the script's range arguments to isolate the exact single row index (0-based) in `data.csv` that triggers the instability.

When you have found the missing linker flag and the problematic row index, write your findings to `/home/user/report.txt` in exactly the following format:
```
Missing library: <name_of_the_library>
Failing row index: <integer>
```

(For example, if the missing library was `z` and the failing row was `999`, you would write `Missing library: z` and `Failing row index: 999`).