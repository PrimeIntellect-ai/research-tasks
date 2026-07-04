You are a data analyst debugging an ETL and evaluation pipeline. 

You have two datasets in `/home/user/data/`:
1. `features.csv` - Contains an `id` column followed by 3 continuous features (`f1`, `f2`, `f3`).
2. `targets.csv` - Contains an `id` column and a `target` continuous variable.

The rows in these files are NOT in the same order, and some IDs might exist in one file but not the other. 

Your tasks are:
1. **Multi-source Data Joining**: Join the two datasets on the `id` column (inner join). Keep only the rows present in both files. Create a unified dataset at `/home/user/data/joined.csv` containing `id,f1,f2,f3,target` (comma-separated, no headers in the output). Sort the final joined dataset numerically by `id` in ascending order.

2. **ETL & Cross-Validation Pipeline in C++**: Write a C++ program at `/home/user/pipeline.cpp` that reads `joined.csv` and performs exactly 5-fold cross-validation. 
   - Split the data sequentially: Fold 1 is the first 20% of the sorted data, Fold 2 is the next 20%, etc. (Assume the joined dataset size is perfectly divisible by 5).
   - **Crucial Requirement (Avoid Data Leaks)**: For each fold split (Train: 4 folds, Val: 1 fold), standard-scale (z-score normalize) the features `f1, f2, f3`. You MUST compute the mean and standard deviation *only* on the Training folds, and use those exact statistics to normalize both the Training and Validation folds. (Global normalization prior to splitting is a data leak and will fail the test).

3. **Correlation Analysis & Prediction**: 
   - Inside the cross-validation loop, for each training split, compute the Pearson correlation coefficient between each normalized feature and the `target` variable using the training data. This gives you a weight vector $w = [corr(f1, t), corr(f2, t), corr(f3, t)]$.
   - Predict the targets for the Validation fold using the dot product: $\hat{y} = w_1 f1_{val} + w_2 f2_{val} + w_3 f3_{val}$.
   - Compute the Mean Squared Error (MSE) for the Validation fold.

4. **Reporting**:
   - The C++ program should output the average Validation MSE across all 5 folds to standard output.
   - Compile your program (e.g., `g++ -O3 pipeline.cpp -o pipeline`) and run it.
   - Save the final single float value (the average cross-validation MSE, formatted to 4 decimal places) to `/home/user/final_mse.txt`.

Ensure all code is written in standard C++ (no external libraries like Eigen or Boost are allowed). Use basic arrays or `std::vector` for linear algebra operations.