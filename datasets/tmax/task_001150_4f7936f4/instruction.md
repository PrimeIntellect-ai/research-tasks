I am a data scientist fitting a network diffusion model. I have run an MCMC sampler to estimate the posterior distribution of the transmission parameter `theta` for a molecular graph simulation. The samples are saved in `/home/user/samples.csv` (a single column with the header `theta`).

I need you to write a Python script at `/home/user/analyze.py` and execute it to analyze these MCMC samples. The script must do the following:

1. Read the `theta` values from `/home/user/samples.csv`.
2. Calculate the sample mean of `theta`.
3. Compute the 95% bootstrap confidence interval of the mean using the percentile method. 
   - Use exactly `1000` bootstrap resamples. 
   - Set the random seed via `numpy.random.seed(42)` immediately before running the bootstrap loop/function to ensure reproducibility.
4. Fit a Gaussian Kernel Density Estimate (KDE) to the `theta` samples using `scipy.stats.gaussian_kde` with default parameters.
5. Evaluate the log probability density (log PDF) of the fitted KDE at the sample mean.
6. Write the results to `/home/user/results.json` as a JSON object with exactly the following keys:
   - `"mean"`: The sample mean.
   - `"ci_lower"`: The 2.5th percentile of the bootstrap sample means.
   - `"ci_upper"`: The 97.5th percentile of the bootstrap sample means.
   - `"log_pdf_at_mean"`: The log density at the sample mean.

Run your script once it is complete so that `/home/user/results.json` is generated.