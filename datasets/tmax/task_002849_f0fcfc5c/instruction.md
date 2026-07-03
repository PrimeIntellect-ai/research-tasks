You are an AI assistant helping a researcher organize and analyze an experimental dataset. The researcher needs you to clean the data, reduce its dimensionality, and perform Bayesian inference to model the results.

Here is your workflow:

1. **Fix and Install the Modeling Package**: 
   The researcher relies on the `emcee` package for Markov Chain Monte Carlo (MCMC) Bayesian inference. A specific version of the source code has been downloaded to `/app/emcee-3.1.4`, but the researcher accidentally corrupted the installation script while editing it, preventing it from installing. You must find the deliberate error in its `setup.py`, fix it, and install the package into your Python environment.

2. **Data Transformation and Dimensionality Reduction**:
   You have a training dataset at `/home/user/data/train.csv` and a test dataset at `/home/user/data/test.csv`. Both contain 50 continuous feature columns (`f0` to `f49`) and a target column (`target` - only in the train set).
   - Read the training data.
   - Standardize the 50 features (mean of 0, standard deviation of 1).
   - Apply Principal Component Analysis (PCA) to reduce the 50 standardized features down to exactly 3 principal components. 
   - Note: Apply the exact same scaling and PCA transformation to the test data.

3. **Bayesian Inference**:
   Construct a Bayesian linear regression model using the 3 principal components to predict the `target`. 
   The model is: `target = alpha + beta_1*PC1 + beta_2*PC2 + beta_3*PC3`.
   - Use `emcee` to sample the posterior distributions of the parameters (`alpha`, `beta_1`, `beta_2`, `beta_3`). Assume uninformative uniform priors.
   - Run the MCMC sampler for at least 2000 steps with 32 walkers. Discard the first 500 steps as burn-in.
   - Calculate the posterior mean for each parameter.

4. **Prediction and Reporting**:
   - Using the posterior mean parameters, predict the target values for the test set (`/home/user/data/test.csv`).
   - Save the predictions to a plain text file at `/home/user/predictions.txt`, with one floating-point prediction per line, corresponding to the rows of the test set in order.

Ensure your entire workflow is reproducible and written in Python. Your final predictions will be evaluated by an automated script using Mean Squared Error (MSE).