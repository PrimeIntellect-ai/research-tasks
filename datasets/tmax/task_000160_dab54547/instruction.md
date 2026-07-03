You are a machine learning engineer preparing a training dataset for a matrix factorization model. Your pipeline occasionally fails due to near-singular inputs where an observation has zero variance across all its features. 

You have been given a dataset stored in HDF5 format at `/home/user/data/samples.h5`. 
This file contains two datasets:
1. `/observations`: A 2D matrix of shape (100, 5) representing 100 samples, each with 5 observational features.
2. `/mcmc_samples`: A 2D matrix of shape (100, 1000) representing 1000 MCMC posterior draws for a specific parameter associated with each of the 100 samples.

Your task is to identify the anomalous sample and estimate its posterior mean using standard Linux CLI tools. You must use `bash`, `h5dump`, `awk`, and other standard Unix utilities. Do not write a Python or R script to solve this; the goal is to accomplish this using shell-based data processing.

Perform the following steps:
1. Identify the 0-based row index in `/observations` where all 5 features have the exact same numerical value (causing a near-singular input for the factorization step).
2. Extract the 1000 MCMC samples corresponding to that specific row index from the `/mcmc_samples` dataset.
3. Compute the posterior mean (the average) of those 1000 MCMC samples.
4. Save the results to `/home/user/anomaly_report.txt` in the exact format:
`Row: <index>, Posterior Mean: <mean rounded to 2 decimal places>`

Example of the expected output format:
`Row: 42, Posterior Mean: 1.23`