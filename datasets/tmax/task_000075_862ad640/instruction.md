You are an AI assistant helping a data scientist fit and compare models.

We have an image of some notes at `/app/params.png`. It contains the parameters for a target Normal distribution in the format `mu=<value> sigma=<value>`.

Your task is to:
1. Extract the parameters from the image (OCR tools like `tesseract` are available).
2. Write a C++ program that performs the following statistical analysis:
   - Simulates 10,000 samples from the Target Normal distribution (using the parameters extracted from the image).
   - Simulates 10,000 samples from a Reference Normal distribution with `mu=4.5` and `sigma=2.0`.
   - Computes the 1st Wasserstein distance between the two empirical samples. (Hint: for 1D samples of the same size, this is the mean of the absolute differences between the sorted samples).
   - Computes a 95% bootstrap confidence interval for this Wasserstein distance using 1,000 bootstrap iterations. In each iteration, resample 10,000 observations with replacement from the target sample, and 10,000 observations with replacement from the reference sample, then compute the Wasserstein distance. The 95% CI corresponds to the 2.5th and 97.5th percentiles of the bootstrap distribution.
3. Expose these results via an HTTP server listening on `127.0.0.1:8080`. You may write the server entirely in C++ (e.g., using `cpp-httplib`), or you may write a Python wrapper (e.g., Flask/FastAPI) that calls your compiled C++ binary to get the results. 
   - The server must accept a `GET` request at the endpoint `/metrics`.
   - The response must be a JSON object with the following keys:
     - `"wasserstein"`: The computed 1st Wasserstein distance.
     - `"ci_lower"`: The lower bound of the 95% bootstrap CI.
     - `"ci_upper"`: The upper bound of the 95% bootstrap CI.

Constraints:
- The core simulation, sorting, and distance metric computations *must* be implemented in C++.
- Set reasonable random seeds in your C++ code to ensure stable results. 
- The evaluation will check your HTTP server's response and expect the values to be statistically sound and within a reasonable tolerance (+/- 0.05) of the true expected values.

Leave the HTTP server running in the foreground or background so the verification system can query it.