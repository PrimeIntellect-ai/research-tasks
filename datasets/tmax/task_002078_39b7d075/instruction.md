You are tasked with debugging and fixing a high-performance mathematical Python extension that is failing its continuous integration tests.

The project is located in `/home/user/project`. It consists of a C extension (`fast_math.c`) wrapped by a Python `setup.py`. We use a proprietary stripped binary oracle, located at `/app/math_oracle`, as the ground truth for our mathematical computations.

Currently, the pipeline is completely broken:
1. The build step is failing with compiler/linker errors when running `python3 setup.py build_ext --inplace`.
2. Even when previous developers managed to compile it, the extension produced incorrect outputs for certain inputs, causing intermittent test failures. 

Your objectives are:
1. **Fix the build:** Identify and resolve the compiler/linker errors in the project so the C extension builds successfully.
2. **Isolate and fix the mathematical bug:** Use the provided `/app/math_oracle` binary to determine where the C extension's logic diverges from the true expected behavior. The oracle takes a single float argument (e.g., `/app/math_oracle 3.14`) and prints the result. You may need to write a quick delta-debugging script to find the inputs that trigger the bug. Modify `fast_math.c` to fix the issue.
3. **Generate the final output:** Once fixed, write a Python script `/home/user/run_all.py` that imports your fixed extension, reads a list of 10,000 floats from `/home/user/project/inputs.csv` (one per line), and writes the computed results to `/home/user/predictions.txt` (one float per line).

The automated verifier will evaluate `/home/user/predictions.txt` against the ground-truth outputs using the Mean Squared Error (MSE) metric. To pass this task, your outputs must achieve an MSE strictly less than 1e-7 compared to the oracle.

Ensure your Python script runs efficiently and generates exactly 10,000 lines in the output file.