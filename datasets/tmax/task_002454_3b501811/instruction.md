You are a data scientist analyzing spectroscopy signals. We need to evaluate the numerical stability of our MCMC peak-fitting model by injecting varying levels of noise into a baseline signal and observing how the estimated peak center ($\mu$) changes. 

I have provided a base dataset at `/home/user/base_data.csv` (with headers `x,y`) and a parameterized Jupyter notebook `/home/user/mcmc_template.ipynb` that performs the MCMC sampling to fit a Gaussian peak.

Your task is to create a reproducible Bash orchestration pipeline. Write a Bash script at `/home/user/run_stability_test.sh` that performs the following steps:

1. **Dependency Management**: Ensure `papermill`, `jupyter`, `pandas`, `scipy`, and `jq` are installed in your Python environment.
2. **Noise Injection**: For each noise level $\sigma \in \{0.1, 0.2, 0.3, 0.4, 0.5\}$, generate a new dataset `/home/user/data_noise_<sigma>.csv` by adding Gaussian noise (mean 0, standard deviation $\sigma$) to the `y` values of `base_data.csv`. Use a fixed random seed for this injection (e.g., seed=42) to ensure reproducibility.
3. **Notebook Orchestration**: Use `papermill` to execute `mcmc_template.ipynb` for each generated dataset. 
   - The notebook takes two parameters: `input_file` (the path to the noisy CSV) and `output_json` (the path to save the MCMC results).
   - Save the executed notebook as `/home/user/mcmc_run_<sigma>.ipynb`.
   - The output JSON for each run should be saved to `/home/user/result_<sigma>.json`.
4. **Result Aggregation**: Use `jq` to extract the `estimated_mu` value from each JSON file.
5. **Reporting**: Compile the results into a tab-separated values file at `/home/user/summary.tsv`. The file must have exactly this header: `NoiseLevel\tEstimatedMu`. Append the results sorted by noise level ascending.

Constraints:
- Your script `/home/user/run_stability_test.sh` must be executable (`chmod +x`).
- Use standard Bash tools (`jq`, `awk`, loops) and lightweight inline Python for the noise injection if necessary.
- Run the script so that the final `summary.tsv` is generated.