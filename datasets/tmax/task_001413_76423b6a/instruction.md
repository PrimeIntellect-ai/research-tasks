I am a researcher working on simulating high-energy particle interactions. I have been trying to perform density estimation on my simulated feature sets by fitting a Multivariate Normal (MVN) distribution using Maximum Likelihood Estimation (MLE). However, my dataset contains highly collinear features, resulting in a near-singular sample covariance matrix. This causes my likelihood calculations and precision matrix inversions to fail or become numerically unstable.

I have an image of a lab note containing a regularization parameter that should stabilize the covariance matrix. 

Please perform the following workflow:

1. **Environment Setup**: Create a Python virtual environment at `/home/user/venv`. Install necessary scientific and image processing libraries (e.g., `numpy`, `scipy`, `Pillow`, `pytesseract`). Note that the `tesseract-ocr` system package is already available. Activate this environment for your work.
2. **Parameter Extraction**: Extract the Tikhonov regularization parameter ($\lambda$) from the image located at `/app/reg_param.png`. 
3. **Model Fitting**: Load the training data from `/app/train_data.npy`. This is an $N \times D$ array. Fit two distinct Multivariate Normal models to this data:
   * **Model 1 (Regularized Full Covariance)**: Compute the sample mean $\mu$ and sample covariance $\Sigma_{sample}$. Calculate the regularized covariance matrix $\Sigma_{reg} = \Sigma_{sample} + \lambda I$, where $I$ is the identity matrix and $\lambda$ is the extracted parameter.
   * **Model 2 (Diagonal Covariance)**: Assume features are independent. Compute a diagonal covariance matrix $\Sigma_{diag}$ whose diagonal entries are the variances of each feature from the training data. All off-diagonal elements are exactly zero.
4. **Hypothesis Comparison**: Compute the Bayesian Information Criterion (BIC) for both models on the training data. 
   * Formula: $\text{BIC} = k \ln(N) - 2 \ln(\hat{L})$
   * $N$ is the number of training samples.
   * $k$ is the number of estimated parameters. For Model 1 (Full Covariance), $k = D + \frac{D(D+1)}{2}$. For Model 2 (Diagonal Covariance), $k = D + D$.
   * $\hat{L}$ is the maximized likelihood of the data given the model.
5. **Evaluation**: Identify the better model (the one with the *lower* BIC). Compute the Negative Log-Likelihood (NLL) of this chosen model on the held-out test dataset located at `/app/test_data.npy`. NLL should be the sum of the negative log probability densities of all test samples.
6. **Final Integration**: Create a Python script at `/home/user/evaluate_models.py` that, when executed, produces a JSON file at `/home/user/results.json` containing exactly the following keys:
   * `"lambda_extracted"`: (float) the parameter extracted from the image.
   * `"bic_model1_full_reg"`: (float) BIC for the regularized full covariance model.
   * `"bic_model2_diag"`: (float) BIC for the diagonal model.
   * `"best_model_test_nll"`: (float) the NLL of the best model on the test data.

Your final output must be the functional `/home/user/evaluate_models.py` script and the resulting `/home/user/results.json` file.