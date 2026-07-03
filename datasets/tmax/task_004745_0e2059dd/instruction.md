You are an Machine Learning Engineer preparing training data for a probabilistic model. As part of your data validation pipeline, you need to estimate the uncertainty of your dataset's mean using bootstrap sampling, and then calculate a Bayesian posterior estimate of the mean to use as a prior for a downstream model.

You have a dataset at `/home/user/data.csv` consisting of 100 integer values (one per line). 
You also have a C program at `/home/user/stats_calc.c` that is supposed to calculate these statistics. However, similar to a plotting script that produces blank plots due to a misconfigured backend, this C script is failing to capture the continuous variance of the bootstrap samples. It appears to be outputting discrete, truncated values for the bootstrap means, completely ruining the confidence interval estimates.

Your task:
1. Identify and fix the bug in `/home/user/stats_calc.c`. The program must correctly compute continuous (double-precision) means for each bootstrap sample.
2. The program must use `srand(42);` exactly once before the bootstrap loop for reproducibility. (This is already in the file, do not remove it).
3. The program performs 10,000 bootstrap iterations (sampling with replacement). It then calculates the 95% Confidence Interval (the 2.5th percentile and 97.5th percentile of the sorted bootstrap means).
4. The program also calculates the Bayesian Posterior Mean of the original dataset. It assumes a Normal-Normal conjugate model with a prior mean $\mu_0 = 50.0$, prior variance $\sigma_0^2 = 25.0$, and known data variance $\sigma^2 = 100.0$. 
5. Compile your fixed C program: `gcc /home/user/stats_calc.c -o /home/user/stats_calc -lm`
6. Run the compiled program and save its standard output EXACTLY to `/home/user/results.txt`.

The expected output format of the C program (and thus the contents of `/home/user/results.txt`) should be exactly:
```
Bootstrap 95% CI: [lower_bound, upper_bound]
Posterior Mean: value
```
Where `lower_bound`, `upper_bound`, and `value` are formatted to 3 decimal places (e.g., `53.123`).