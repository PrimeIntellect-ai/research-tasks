You are a data engineer building an ETL and model-tuning pipeline entirely in Bash. 

We have a mock model training script located at `/home/user/train_model.sh` that takes two arguments: the path to the dataset, and a regularization parameter (a float). The script relies on the numerical environment variable `OPENBLAS_NUM_THREADS` to determine how many CPU threads to use for its internal matrix operations. It prints a single floating-point number representing the cross-validation error of the model.

Your task is to write and execute a Bash script `/home/user/optimize.sh` that performs hyperparameter tuning (a grid search) to find the optimal configuration that minimizes the cross-validation error.

Here are your specific instructions:
1. Large-scale data staging: A compressed dataset is located at `/home/user/raw_data.tar.gz`. Extract its contents into the directory `/home/user/data/` (you will need to create this directory). Inside the archive is a file named `dataset.csv`.
2. Grid Search: Write a bash script `/home/user/optimize.sh` that loops over the following hyperparameter combinations:
   - Thread counts (`T`): 1, 2, 4, 8
   - Regularization (`R`): 0.01, 0.1, 1.0, 10.0
3. For each combination, your script must:
   - Set the `OPENBLAS_NUM_THREADS` and `OMP_NUM_THREADS` environment variables to the current thread count `T`.
   - Execute `/home/user/train_model.sh /home/user/data/dataset.csv <R>`
   - Capture the resulting cross-validation error.
4. After testing all combinations, determine which combination of `T` and `R` produced the lowest error.
5. Write this best configuration to `/home/user/best_params.csv`. The file must have exactly two lines: a header line `threads,reg,error` and a second line with the optimal values (e.g., `2,0.1,0.5000`).

Ensure your `/home/user/optimize.sh` script is executable and run it to produce the final `/home/user/best_params.csv` file.