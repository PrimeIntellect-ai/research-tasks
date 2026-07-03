You are a performance engineer profiling a microservice whose theoretical latency model was lost. Fortunately, we recovered a screenshot of the model's parameters at `/app/system_model.png`.

Your task is to extract these parameters, write a Go-based performance analysis API, and expose endpoints to evaluate the system using Monte Carlo simulation, numerical integration, and statistical hypothesis testing.

1. **Extract Parameters:** Use an OCR tool (like `tesseract`) to read `/app/system_model.png`. The image contains three values for the theoretical normal distribution of the system's latency: `mu` (mean latency in ms), `sigma` (standard deviation in ms), and `threshold` (the SLA failure threshold in ms).

2. **Build the API Server:** Write a Go HTTP server that listens on `127.0.0.1:9090`. 

3. **Implement Endpoints:**
   * **`GET /montecarlo?samples=<int>`**: 
     Generate `samples` number of independent random values drawn from a normal distribution using the extracted `mu` and `sigma`. Return the empirical probability of the latency strictly exceeding the `threshold`. 
     Response format: `{"mc_prob": 0.0123}` (JSON).

   * **`GET /integrate`**: 
     Use a numerical integration method (e.g., trapezoidal rule, Simpson's rule, or exact CDF calculation using `math.Erfc`) on the probability density function (PDF) of the normal distribution to compute the exact theoretical probability of latency > `threshold`.
     Response format: `{"exact_prob": 0.0123}` (JSON).

   * **`GET /test`**:
     Read the actual application latency data from `/app/profiling_data.csv`. This file contains a single column of float values (one latency measurement per line) without a header.
     Perform a one-sample Z-test to compare the sample mean of the profiling data against the theoretical population mean (`mu`) using the theoretical population standard deviation (`sigma`). Calculate the Z-score using the formula: `Z = (SampleMean - mu) / (sigma / sqrt(N))`.
     Response format: `{"z_score": 1.5432}` (JSON).

Make sure your Go server is compiled and running in the background listening on `127.0.0.1:9090` so the verifier can issue requests to it. Do not require any authentication.