You are an AI assistant helping a scientific researcher organize and analyze a collection of experimental datasets. 

The researcher has left several raw data files in the directory `/home/user/datasets/`. You need to write and execute a Python script to process this data, perform Bayesian inference, and extract features using linear algebra.

Here are your instructions:

1. **Environment Setup**: Ensure `pandas` and `numpy` are installed. You may install them using `pip` if they are not present.

2. **Data Aggregation**: 
   - Read all CSV files located in `/home/user/datasets/`. They all share the same schema: `experiment_id`, `group`, `trials`, `successes`, `f1`, `f2`, `f3`.
   - Concatenate them into a single dataset.
   - Group the data by the `group` column.
   - For each group, calculate the total sum of `trials` and the total sum of `successes`.
   - For each group, calculate the mean of the continuous features: `f1`, `f2`, and `f3`.

3. **Bayesian Inference**:
   - The researcher wants to estimate the true success rate for each group. 
   - Assume a Binomial likelihood for the number of successes given the trials, and a uniform Beta(1, 1) prior for the success probability.
   - For each group, calculate the **posterior mean** of the success probability.

4. **Linear Algebra (Dimensionality Reduction)**:
   - Construct a matrix $X$ using the aggregated mean values of `f1`, `f2`, and `f3`. The rows of $X$ should correspond to the groups, sorted alphabetically by the group name (e.g., 'A', 'B', 'C'). The columns should be `f1`, `f2`, and `f3` in that order.
   - Mean-center the columns of matrix $X$ (subtract the column means from each column).
   - Compute the first principal component (the right singular vector corresponding to the largest singular value) of the centered matrix $X$ using Singular Value Decomposition (SVD). 
   - To ensure a deterministic output, if the first element of this principal component vector is negative, multiply the entire vector by -1.

5. **Reporting**:
   - Save your final results to a JSON file at `/home/user/analysis_report.json`.
   - The JSON file must have exactly this structure:
     ```json
     {
       "posterior_means": {
         "GroupA": 0.543,
         "GroupB": 0.123,
         ...
       },
       "first_pc": [0.123, 0.456, 0.891]
     }
     ```
   - All floating-point numbers should be kept at standard precision; do not round them manually in the JSON.