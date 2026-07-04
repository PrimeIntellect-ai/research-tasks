I am a physics researcher running particle simulations, and I need a reproducible C++ pipeline to analyze the energy distributions of the simulated particles. 

I have generated an HDF5 file located at `/home/user/sim_data.h5`. Inside this file, there is a 1D dataset named `/energies` containing 10,000 floating-point (double) values. 

Your task is to write a C++ program (`/home/user/analyze_energies.cpp`) that reads this HDF5 dataset and performs statistical hypothesis comparison to determine the best-fitting probability distribution for the energies. 

Specifically, you must:
1. Read the dataset `/energies` from `/home/user/sim_data.h5` into a C++ vector.
2. Compute the sample mean ($\mu$) and sample variance ($\sigma^2$) of the data. Use the unbiased sample variance formula (divide by $N-1$).
3. We are comparing two hypotheses for the underlying distribution:
   - **Hypothesis A (Gaussian):** The data follows a Normal distribution $N(\mu, \sigma^2)$ parameterized by the sample mean and sample variance.
   - **Hypothesis B (Exponential):** The data follows an Exponential distribution $Exp(\lambda)$ where the rate parameter $\lambda = 1 / \mu$.
4. Calculate the Log-Likelihood ($LL$) of the entire dataset under *both* distributions. 
   - Gaussian PDF: $f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$
   - Exponential PDF: $f(x) = \lambda e^{-\lambda x}$
5. Calculate the Akaike Information Criterion (AIC) for both models. $AIC = 2k - 2(LL)$, where $k$ is the number of estimated parameters ($k=2$ for Gaussian, $k=1$ for Exponential).
6. Determine the "best_fit" distribution, which is the one with the **lower** AIC value.
7. Write the results to a JSON file at `/home/user/analysis_results.json` with the exact following structure and keys (values should be printed to at least 4 decimal places):

```json
{
  "mean": 5.1234,
  "variance": 1.2345,
  "log_likelihood_gaussian": -1234.5678,
  "log_likelihood_exponential": -2345.6789,
  "aic_gaussian": 2473.1356,
  "aic_exponential": 4693.3578,
  "best_fit": "gaussian"
}
```

Compile your C++ program to an executable `/home/user/analyze_energies` and run it to produce the JSON file. You will need to link against the HDF5 C++ libraries (`-lhdf5_cpp -lhdf5`). Do not use any external statistics libraries (like Boost) for the likelihood calculations; implement the formulas directly in your C++ code using standard `<cmath>`.