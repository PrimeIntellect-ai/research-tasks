You are assisting a researcher running material science simulations.

We received a scanned configuration image from the lab, located at `/app/config.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. It contains the baseline parameters `alpha` and `beta` for our simulation.

We have a C program at `/home/user/sim.c` that simulates the material's stress-strain curve. 
1. Compile the C code (e.g., using `gcc`).
2. Run the compiled executable, passing the extracted `alpha` and `beta` values as command-line arguments in that order (e.g., `./sim <alpha> <beta>`).
3. The program will output deterministic simulated data to `stdout` as two space-separated columns: `X` (strain) and `Y` (stress with experimental noise). Capture this output.

Once you have the data:
1. Fit a simple linear regression model ($Y = mX + c$) to the generated data to find the slope ($m$).
2. Calculate the 95% bootstrap confidence interval for the slope $m$. Use exactly 1000 resamples and the percentile method. To ensure reproducible results, use Python with `numpy` for this step, and strictly set `numpy.random.seed(123)` immediately before performing the bootstrap resampling.

Finally, expose your results to our automated testing framework:
Write and start a simple HTTP server (you can use Python's Flask, FastAPI, or `http.server`) listening on `0.0.0.0` at port `8080`.
When a `GET` request is made to the endpoint `/api/result`, the server must return a JSON response with exactly these keys:
- `"slope"`: The calculated line of best fit slope (float, rounded to 3 decimal places)
- `"ci_lower"`: The lower bound of the 95% bootstrap confidence interval (float, rounded to 3 decimal places)
- `"ci_upper"`: The upper bound of the 95% bootstrap confidence interval (float, rounded to 3 decimal places)

Keep the server running in the background so the verifier can access it.