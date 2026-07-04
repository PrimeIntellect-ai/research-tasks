You are an ML engineer preparing a synthetic training dataset for a new probabilistic model. We have lost the original source data, but we recovered a screenshot of a legacy report containing the Bayesian prior parameters (Mean vector and Covariance matrix) for the historical data features.

The screenshot is located at `/app/legacy_report.png`. 

Your task is to:
1. Extract the statistical priors (Mean vector and Covariance matrix) from the image. You may use `tesseract` or any other tool, or transcribe it if you prefer, but you must automate the data generation pipeline.
2. Set up a Go module in `/home/user/data_gen/` and configure the necessary numerical libraries (we strongly recommend `gonum.org/v1/gonum/mat` and `gonum.org/v1/gonum/stat/distmv`).
3. Write a Go program (`/home/user/data_gen/main.go`) that uses these extracted prior parameters to sample exactly 50,000 synthetic data points from a Multivariate Normal distribution. Linear algebra operations (like Cholesky decomposition) might be required depending on the library used.
4. Experiment Tracking: Log the extracted parameters and generation timestamps into a file `/home/user/data_gen/experiment_log.json`.
5. Model Output Validation: Write the 50,000 generated samples to `/home/user/data_gen/synthetic_data.csv`. The CSV should have headers `f1,f2,f3` corresponding to the three dimensions.

Your final generated dataset will be evaluated strictly on how well its empirical statistics (mean and covariance) match the target priors extracted from the image. Ensure your numerical configuration and sampling logic are correct.