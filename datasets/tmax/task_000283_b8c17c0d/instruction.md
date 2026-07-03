You are a data scientist taking over a project where a colleague left an incomplete and buggy analysis script. Your workspace is located at `/home/user/project`.

Inside this directory, there is a dataset `data.csv` containing a single column `value`. This dataset contains extreme outliers and missing values (`NaN`).

Your task is to write a Python script `/home/user/project/clean_and_analyze.py` that performs the following steps:

1. **Outlier Handling**: Read `data.csv`. Calculate the First Quartile (Q1) and Third Quartile (Q3) of the non-NaN values. Compute the Interquartile Range ($IQR = Q3 - Q1$). Remove any rows where the value is strictly less than $Q1 - 1.5 \times IQR$ or strictly greater than $Q3 + 1.5 \times IQR$.
2. **Bootstrap Imputation**: Count the number of `NaN` values originally present. Replace these `NaN` values by sampling with replacement from the *cleaned* (non-NaN, non-outlier) data. 
   *Constraint*: Use `numpy.random.RandomState(42).choice(cleaned_values, size=num_nans, replace=True)` to ensure reproducible imputation. Append these imputed values to your cleaned data array to form the `final_dataset`.
3. **Bayesian Inference & Hyperparameter Tuning**: Assume the `final_dataset` is drawn from a Normal distribution with an unknown mean $\mu$ and a known variance $\sigma^2 = 1.0$. Assume a Normal prior for $\mu \sim \mathcal{N}(0, \alpha^2)$. 
   The posterior distribution for $\mu$ will also be Normal: $\mathcal{N}(\mu_{post}, \sigma^2_{post})$.
   Use leave-one-out cross-validation (LOOCV) over the `final_dataset` to evaluate the prior standard deviation $\alpha \in [1.0, 5.0, 10.0]$. For each LOOCV fold (leaving out $x_i$), compute the posterior predictive mean $\mu_{pred}$ using the remaining data, and calculate the squared error $(x_i - \mu_{pred})^2$. 
   Select the $\alpha$ that minimizes the Average Mean Squared Error across all LOOCV folds.
4. **Export Results**: Save a JSON file at `/home/user/project/results.json` containing:
   - `"best_alpha"`: The optimal $\alpha$ chosen.
   - `"posterior_mean"`: The posterior mean $\mu_{post}$ computed on the *entire* `final_dataset` using the `best_alpha`.
   - `"posterior_variance"`: The posterior variance $\sigma^2_{post}$ computed on the *entire* `final_dataset` using the `best_alpha`.
   *(Round all floating point values in the JSON to 4 decimal places).*
5. **Plotting**: Create a plot of the final posterior PDF using `matplotlib.pyplot` and save it to `/home/user/project/posterior.png`. Ensure the plot actually renders to the file (your colleague's previous script produced blank images due to a backend/saving misconfiguration—make sure your script saves it properly using a non-interactive backend like `Agg`).

**Note**: You must create the `data.csv` file yourself to test your script. The real evaluation environment will have a `data.csv` pre-populated with unseen values. Ensure your code is robust.