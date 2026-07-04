You are an AI assistant helping a data scientist validate the convergence of a sampling algorithm. 

We have a Jupyter notebook located at `/home/user/sampler.ipynb` that acts as a Monte Carlo sampler. However, it hasn't been executed yet.

Your task is to orchestrate this workflow and perform a convergence test against an analytical solution:

1. Execute the notebook `/home/user/sampler.ipynb` headlessly in the terminal. The notebook will automatically generate a file named `/home/user/samples.txt` containing 10,000 float values (one per line).
2. The samples are theoretically drawn from an Exponential distribution with a rate parameter of $\lambda = 2.0$ (Note: in scipy, scale = $1/\lambda = 0.5$).
3. Write a Python script at `/home/user/evaluate.py` that validates the convergence of these samples. Your script must:
    - Read the generated `/home/user/samples.txt`.
    - For $N \in [1000, 5000, 10000]$, take the *first* $N$ samples.
    - Use `scipy.stats.kstest` to compute the Kolmogorov-Smirnov (KS) statistic (which measures the maximum distance between the empirical CDF and the analytical CDF) comparing the $N$ samples to the exact analytical Exponential distribution ($\lambda = 2.0$).
    - Save the results to `/home/user/convergence.csv`.
4. The output file `/home/user/convergence.csv` must have exactly the following format (including the header), with the KS statistic rounded to 4 decimal places:
```csv
N,KS
1000,0.xxxx
5000,0.xxxx
10000,0.xxxx
```

Complete this workflow using the terminal and standard scientific Python libraries (numpy, scipy).