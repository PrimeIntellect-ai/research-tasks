You are an ML engineer preparing a synthetic dataset for a new time-series forecasting model. We need a reproducible pipeline to generate, track, and validate this data.

Write a Python script at `/home/user/generate_data.py` that does the following:

1. **Reproducible Pipeline Construction**: Set the `numpy` random seed to `42` to ensure the generated data is reproducible. 
2. **Data Generation**: Generate exactly 1000 samples for a synthetic sensor. 
   - Create an array `x` of 1000 evenly spaced points between $0$ and $10\pi$ inclusive.
   - Generate `y` using the formula: $y = 2.5 \sin(x) + \epsilon$, where $\epsilon$ is Gaussian (normal) noise with a mean of 0.0 and a standard deviation of 0.5.
3. **Model Output Validation**: Calculate the empirical mean and variance of `y`. 
   - If the mean is strictly between -0.2 and 0.2, and the variance is strictly between 2.5 and 4.0, write the string "SUCCESS" to `/home/user/validation.log`.
   - If it fails these conditions, write "FAILED" to the log and exit the script without saving the data.
4. **Experiment Tracking**: Save the configuration parameters to `/home/user/experiment_config.json`. It must be a valid JSON object containing exactly these keys and values:
   - `"seed"`: 42
   - `"num_samples"`: 1000
   - `"noise_mean"`: 0.0
   - `"noise_std"`: 0.5
5. **Output**: If the validation passes, save `x` and `y` to `/home/user/training_data.csv` with the headers `x,y`. 

Run the script so that the CSV, JSON, and log files are generated.