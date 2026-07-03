As a machine learning engineer, you need to prepare a high-performance data processing pipeline in C to generate training data for a new model. The pipeline must join two separate data sources, apply a fixed dimensionality reduction projection, and output a clean dataset.

You have been provided with two CSV files (which you must assume exist, though you may need to write a script to generate dummies if you want to test your code locally before final execution, or just read the structure below):
1. `/home/user/data/sourceA.csv` - Contains columns: `id,f1,f2,f3`
2. `/home/user/data/sourceB.csv` - Contains columns: `id,f4,f5`

Your task:
1. Create a C program at `/home/user/pipeline/process.c` that:
   - Reads both CSV files.
   - Performs an inner join on the `id` column (which is an integer). Assume the files are not necessarily sorted and there may be IDs in one file that do not exist in the other.
   - For the joined records, applies a dimensionality reduction to project the 5 features (`f1` to `f5`) into 2 principal components (`PC1` and `PC2`) using the following fixed weights:
     `PC1 = 0.2*f1 + 0.4*f2 + 0.4*f3 + 0.5*f4 + 0.5*f5`
     `PC2 = -0.5*f1 + 0.5*f2 + 0.0*f3 - 0.5*f4 + 0.5*f5`
   - Writes the output to `/home/user/output/training_data.csv` with the format `id,PC1,PC2`.
   - The output CSV should have a header row `id,PC1,PC2`.
   - The floating point values for PC1 and PC2 must be formatted to exactly one decimal place (e.g., `72.0`).
   - The output rows must be sorted in ascending order by `id`.

2. Write a `Makefile` in `/home/user/pipeline/` with a default target `all` that:
   - Compiles `process.c` into an executable named `process` using `gcc` with `-O3`.
   - Runs the `process` executable to generate `/home/user/output/training_data.csv`.

Ensure all directories exist or are created by your Makefile/program if they don't. The test will verify the correctness of `/home/user/output/training_data.csv` after invoking `make -C /home/user/pipeline`.