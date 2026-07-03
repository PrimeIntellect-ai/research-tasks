I am trying to run a data cleaning and model evaluation pipeline, but it is failing silently. Much like a misconfigured visualization script that produces blank plots, my C++ pipeline finishes executing but produces an empty `model_params.txt` file and reports "0 valid records".

I have a pipeline located in `/home/user/pipeline/`. It consists of:
1. A dataset at `/home/user/pipeline/data.csv` containing sensor readings in the format `id,feature,target`.
2. A C++ program `/home/user/pipeline/cleaner.cpp` that is supposed to:
   - Read the dataset path from the `DATASET_PATH` environment variable.
   - Perform bootstrap sampling (using a fixed seed `std::srand(42)`) on the `feature` column to calculate the mean.
   - Filter out records where the feature deviates by more than 10.0 from the bootstrapped mean.
   - Fit a simple linear regression model ($target = m \cdot feature + c$) on the cleaned dataset.
   - Write the parameters `m` and `c` to `/home/user/pipeline/model_params.txt` in the format `m=<value>,c=<value>`.
3. A runner script `/home/user/pipeline/run_pipeline.sh` that compiles and runs the program.

Currently, there are two issues:
1. A system/pipeline configuration issue: The C++ executable exits early because it cannot find the dataset, but the bash script swallows the error.
2. A C++ logic bug: Even when the file is read, an integer division/precision bug in the bootstrap sampling calculation causes the mean to be wildly incorrect, leading the filter step to drop *all* records.

Your task:
- Identify and fix the bugs in `/home/user/pipeline/cleaner.cpp`.
- Fix `/home/user/pipeline/run_pipeline.sh` so it properly configures the environment and executes the pipeline.
- Run `/home/user/pipeline/run_pipeline.sh` so that it successfully outputs the correct model parameters to `/home/user/pipeline/model_params.txt`.