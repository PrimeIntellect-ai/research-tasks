You are a Machine Learning Engineer preparing a structural biology dataset for a new Graph Neural Network. Your pipeline requires extracting pairwise distances between Alpha-Carbon (CA) atoms from a large set of PDB (Protein Data Bank) files to generate summary features (mean, max, and variance of pairwise distances).

To handle the massive scale of our real dataset, we rely on a custom, highly optimized C library called `libfastcontact`. A snapshot of the source code is vendored at `/app/libfastcontact-0.9`.

However, the pipeline is currently broken:
1. The `libfastcontact` package fails to build.
2. Even when previous engineers forced it to compile, the generated features resulted in extremely poor downstream model accuracy (~50%, equivalent to random guessing). We suspect there is a regression in the statistical calculations or parsing logic within the C code itself.

Your objectives:
1. Diagnose and fix the build configuration for `/app/libfastcontact-0.9`.
2. Inspect the C source code, identify the logic bug causing the incorrect feature generation, and fix it.
3. Once fixed and compiled, use the `fastcontact` binary to process all PDB files located in `/app/data/raw_pdbs`. 
4. Write a reproducible pipeline (using Bash or a script of your choice) to reshape the observational data into a single CSV file at `/home/user/training_data.csv`. The CSV must have the following header:
   `pdb_id,mean_dist,max_dist,var_dist,label`
   - `pdb_id`: The filename without the `.pdb` extension (e.g., `protein_01`).
   - `mean_dist`: The mean CA-CA distance output by the tool.
   - `max_dist`: The max CA-CA distance output by the tool.
   - `var_dist`: The variance of the CA-CA distances output by the tool.
   - `label`: `1` if the filename contains `compact`, `0` if it contains `extended`.

Finally, verify your dataset by running the provided evaluation script:
`python3 /app/train_and_eval.py /home/user/training_data.csv`

This script will parse your CSV, train a logistic regression model, and output the cross-validated accuracy. To successfully complete this task, your generated features must allow the model to achieve an accuracy of at least 0.90. Leave the final valid `training_data.csv` in `/home/user/` for the automated test suite to verify.