You are a data engineer tasked with fixing a critical data leakage bug in an ETL pipeline written in C. 

A previous engineer built a high-frequency telemetry processor that reads an audio-encoded sensor stream located at `/app/telemetry.wav`. The pipeline extracts the data, computes the magnitude of the signal, and applies a standardization step (subtracting the mean and dividing by the standard deviation) to prepare the data for an anomaly detection model. 

However, there is a classic data leakage issue: the current C pipeline computes the mean and standard deviation over the *entire* dataset (train + test) before standardization. This causes future information (the test set) to leak into the training transformations.

Your objectives:
1. Review the existing pipeline code at `/home/user/telemetry_processor.c` (you will need to create/extract it based on the scenario, but assume the base task is to write or fix this C code to read 16-bit PCM data from `/app/telemetry.wav`, skipping the 44-byte WAV header).
2. Configure your environment by installing any necessary numerical or audio processing development libraries you might need (e.g., standard math libraries, or you can write raw C).
3. Implement a strict time-based split: the first 70% of the audio samples are the "Train" set, and the remaining 30% are the "Test" set.
4. Calculate the standardizing statistics (mean and standard deviation) **exclusively** on the Train set. 
5. Apply these Train statistics to standardize *both* the Train and Test sets.
6. Perform a simple hypothesis test / confidence interval calculation: compute the 95% confidence interval of the mean for the *standardized Test set* assuming a normal distribution (using z=1.96). Write the sample mean, lower bound, and upper bound to `/home/user/test_stats.txt` (comma-separated: `mean,lower,upper`).
7. Save the standardized Test set (and ONLY the test set) as an array of double-precision floats (`double`) to a binary file at `/home/user/test_features.bin`.

Ensure your pipeline is reproducible and can be compiled with standard GCC. 

Your success will be evaluated by an automated script that calculates the Mean Squared Error (MSE) between your `/home/user/test_features.bin` and the mathematically correct standardized test set. The MSE must be less than `1e-5`.