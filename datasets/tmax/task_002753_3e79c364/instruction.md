You are a Data Scientist fixing a broken data processing pipeline. 

I have a script at `/home/user/pipeline.py` that is supposed to read a dataset from `/home/user/data.csv`, calculate bootstrap confidence intervals for the mean of the 'value' column, run a simple linear model inference on the scaled mean, and generate a plot.

However, the pipeline is failing. It produces a blank or corrupted plot (due to an environment/backend issue), fails to handle messy data (producing `NaN` metrics), and calculates incorrect model predictions due to an omitted normalization step.

Your task is to fix `/home/user/pipeline.py` so that it runs successfully and generates the correct outputs. 

Here are the requirements for the fixes:
1. **Plotting Backend**: Fix the matplotlib configuration so it successfully writes the plot to `/home/user/output_plot.png` in a headless Linux environment.
2. **Missing Data**: Modify the script to explicitly remove missing values (`NaN`s) from the 'value' column *before* performing the bootstrap sampling.
3. **Model Inference / Numerical Accuracy**: The pre-trained model weights in the script (`Weight: 3.2`, `Bias: 1.5`) expect the input to be standard-scaled (Z-score normalization). You must standardize the calculated `mean_val` using the mean and standard deviation of the cleaned 'value' column before calculating the prediction.
4. Do not change the random seed (`np.random.seed(42)`) or the number of bootstrap iterations (`1000`).

When the script runs successfully, it should generate:
1. `/home/user/output_plot.png`
2. `/home/user/metrics.txt` with exactly the following format:
```
Mean: <calculated_bootstrap_median_to_2_decimal_places>
CI: <lower_ci_to_2_decimals>-<upper_ci_to_2_decimals>
Prediction: <scaled_prediction_to_2_decimals>
```