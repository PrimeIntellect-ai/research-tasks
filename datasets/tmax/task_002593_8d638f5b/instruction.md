You are tasked with fixing a critical data leakage bug in a custom C++ data preprocessing pipeline. 

A data science team has built a high-performance C++ tool to perform Min-Max scaling on large datasets. However, their model's validation scores are suspiciously high. They suspect data leakage: the current C++ implementation computes the minimum and maximum values for scaling over the *entire* dataset (both training and testing rows combined) before applying the transformation.

Your task is to fix this data leak, set up the analysis environment, compile the fixed code, and run a reproducible experiment pipeline.

**Environment Setup & Files:**
The project is located at `/home/user/pipeline/`. You will find the following structure:
- `/home/user/pipeline/data/dataset.csv`: The input dataset. The first column is `id`, the second is `feature_1`, and the third is `is_train` (1 for training set, 0 for testing set).
- `/home/user/pipeline/src/normalize.cpp`: The buggy C++ source code.
- `/home/user/pipeline/CMakeLists.txt`: Build configuration.
- `/home/user/pipeline/run_experiment.sh`: A shell script meant to track and execute the pipeline.

**Requirements:**
1. **Fix the C++ Code**: Modify `/home/user/pipeline/src/normalize.cpp` so that the `min` and `max` values used for Min-Max scaling are computed **exclusively** from the rows where `is_train == 1`. 
2. **Apply Scaling**: Apply the transformation `(value - train_min) / (train_max - train_min)` to **all** rows (both train and test) using the `train_min` and `train_max` derived in step 1.
3. **Experiment Tracking**: Modify the C++ code to print the computed training min and max to standard output in exactly this format: `Feature 1: min=<val>, max=<val>`.
4. **Build the Tool**: Create a `/home/user/pipeline/build/` directory, run CMake, and compile the tool. The executable must be named `normalize_tool`.
5. **Reproducible Pipeline**: Modify `/home/user/pipeline/run_experiment.sh` to:
   - Run the compiled `normalize_tool`.
   - Read `/home/user/pipeline/data/dataset.csv`.
   - Output the transformed data to `/home/user/pipeline/output/normalized.csv` (with columns `id,feature_1_scaled,is_train`).
   - Redirect the standard output (the min/max metrics log) to `/home/user/pipeline/output/metrics.log`.

Make sure the output directory exists before running the script. Execute `run_experiment.sh` so the final output files are generated.