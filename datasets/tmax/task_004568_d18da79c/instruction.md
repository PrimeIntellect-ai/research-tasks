You are a performance engineer analyzing cache miss anomalies in a high-throughput distributed database. A custom monitoring tool has output a visual representation of cache misses over time as a video file, located at `/app/system_monitor.mp4`. 

Your goal is to extract this data, fit a statistical distribution to it using C, and serve the results via an HTTP API.

Step 1: Data Extraction
The video `/app/system_monitor.mp4` contains exactly 120 frames. Each frame represents a single sampling interval. In each frame, the background is completely black, and a certain number of pixels are pure white (`#FFFFFF`). The number of pure white pixels in a frame exactly equals the number of cache misses during that interval.
Extract the cache miss count for all 120 frames to create your dataset.

Step 2: Distribution Fitting (C implementation)
We hypothesize that the cache misses follow a Gamma distribution. You must write a C program (e.g., `fit_gamma.c`) that estimates the shape parameter ($k$) and scale parameter ($\theta$) of the Gamma distribution using Maximum Likelihood Estimation (MLE).
- The MLE for the Gamma distribution requires solving a nonlinear equation involving the natural logarithm and the digamma function. 
- Implement a Newton-Raphson solver in your C program to find the root and estimate $k$. 
- Use a convergence criterion where the absolute difference in $k$ between iterations is less than $1e-6$.
- You may install and link against the GNU Scientific Library (GSL) to access the digamma and trigamma functions (`gsl_sf_psi` and `gsl_sf_psi_1`).
- The program should output the final estimated $k$ and $\theta$.

Step 3: Visualization
Create a Python script that uses the data and the estimated parameters to generate a plot saved at `/home/user/fit_plot.png`. The plot must show a density histogram of the extracted cache miss counts overlaid with the probability density function (PDF) curve of the fitted Gamma distribution.

Step 4: API Service
Create an HTTP server listening exactly on `127.0.0.1:8000`. You may write this server in Python, but it must serve the mathematical parameters derived by your C program.
The server must enforce authentication. Every request must include the header:
`Authorization: Bearer perf-token-2024`
Requests without this header or with an incorrect token must receive a `401 Unauthorized` response.

The server must implement the following endpoints:
1. `GET /params`
   Returns a JSON object with the fitted parameters:
   `{"k": <float>, "theta": <float>}`
2. `GET /pdf?x=<float>`
   Returns the probability density of the fitted Gamma distribution at the given value of `x`.
   `{"pdf": <float>}`

Keep the server running in the background or foreground so that it can be tested. Leave a file named `/home/user/server_ready.txt` once your server is up and running.