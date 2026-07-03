You are an AI assistant helping a data scientist debug a model-fitting pipeline.

You have been provided with a directory at `/home/user/spectroscopy_project` containing a reproducible computation pipeline for analyzing noisy spectroscopy signals. The pipeline attempts to fit a Gaussian model (representing a spectral peak) to the data by minimizing the Kullback-Leibler (KL) divergence between the observed signal distribution and the model.

The project contains the following files:
- `generate_data.py`: Generates the synthetic noisy signal and saves it to `data.csv`.
- `loss.py`: A utility that takes `mu` and `sigma` as command-line arguments, reads `data.csv`, computes the KL divergence, and prints three space-separated values to stdout: `loss`, `grad_mu`, and `grad_sigma`.
- `optimize.sh`: A Bash script that performs gradient descent to find the optimal `mu` and `sigma`.
- `pipeline.sh`: A wrapper script that runs data generation and then the optimization.

**The Problem:**
Currently, `optimize.sh` diverges because it uses a fixed, excessively large learning rate (`lr=2.0`). The parameters quickly overshoot into invalid ranges (like negative standard deviation), causing the script to output `NaN`s and fail the regression tests.

**Your Task:**
1. Rewrite the gradient descent logic in `/home/user/spectroscopy_project/optimize.sh` (using Bash as the primary language, though tools like `awk` or `bc` are highly recommended for floating-point math).
2. Implement the following adaptive step-size algorithm (backtracking line search) to fix the divergence:
   - Initialize `mu=4.0`, `sigma=1.0`, and `lr=1.0`.
   - Calculate the initial loss and gradients.
   - For up to 100 *iterations*:
     - Attempt a step: `new_mu = mu - lr * grad_mu` and `new_sigma = sigma - lr * grad_sigma`.
     - Calculate the `new_loss` at `new_mu` and `new_sigma`.
     - If `new_loss < loss`: Accept the step. Update `mu = new_mu`, `sigma = new_sigma`, `loss = new_loss`, and get the new gradients.
     - If `new_loss >= loss`: Reject the step. Do not update `mu` or `sigma`. Instead, shrink the learning rate: `lr = lr * 0.5`.
     - If `lr < 1e-5`, terminate the optimization early.
3. Save the final optimized parameters in `/home/user/spectroscopy_project/results.txt` in exactly this format:
```
mu=<final_mu>
sigma=<final_sigma>
loss=<final_loss>
```
4. Run `bash pipeline.sh` to execute your fixed pipeline and generate the `results.txt` file.

Ensure your `results.txt` contains valid numbers (not `NaN`) and that the final loss is significantly minimized.