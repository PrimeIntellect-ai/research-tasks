You are a Machine Learning Engineer preparing a pipeline to benchmark classification and regression models. Your task involves fixing a broken vendored package, and writing an optimized data preparation script.

Step 1: Fix and Compile libsvm
We have vendored the source code for `libsvm-3.32` at `/app/libsvm-3.32`. However, a junior developer made an erroneous change to the `Makefile` which prevents it from compiling.
- Identify the error in `/app/libsvm-3.32/Makefile`, fix it, and successfully compile the package.

Step 2: Implement L2 Normalization and Format Conversion
Write a program or script that converts dense CSV datasets into the sparse `libsvm` format while applying L2 normalization to the features. 
- Create an executable shell script at `/home/user/run_scale.sh` that takes two arguments: an input CSV path and an output text file path. `run_scale.sh` should execute your data preparation code (which you can write in Python, C, or any standard language available on Ubuntu).
- **Input Format:** A dense CSV file (no header) where each row contains float values. The **last** column is the target label.
- **Processing:** For each row, calculate the L2 norm (Euclidean norm) of the feature vector (all columns except the last). Divide each feature by this L2 norm. If the L2 norm is 0, leave the features as 0.
- **Output Format:** The standard `libsvm` format: `<label> 1:<feat1> 2:<feat2> ...`
  - Ensure labels and features are formatted to exactly 6 decimal places (e.g., `%.6f`).
  - **Omit** any features that are exactly `0.000000` after formatting.
  - The feature indices are 1-based.

Step 3: Benchmark Test
- To ensure your pipeline works, use your `/home/user/run_scale.sh` to process a dummy dataset (you can create one), then run `/app/libsvm-3.32/svm-train` on the output to verify that `libsvm` accepts the format and successfully trains a model.

The automated verification will specifically test your `/home/user/run_scale.sh` script against a private oracle using a rigorous fuzzing process with numerous randomly generated CSVs to ensure bit-exact equivalence.