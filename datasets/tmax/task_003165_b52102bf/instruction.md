You are a data scientist tasked with analyzing a legacy physical model provided as a compiled binary. 

You have been given a dataset of observation points in an HDF5 file located at `/home/user/experiment.h5`. The file contains a single dataset named `measurements`, which is a 1D array of float values.

There is also a legacy model binary at `/app/model_exec`. This is a stripped binary that takes a single floating-point number as a command-line argument and prints the evaluated function result to stdout (e.g., `/app/model_exec 2.5`).

Your task is to:
1. Extract the `measurements` from the HDF5 file.
2. For each $x$ in `measurements`, compute the numerical derivative of the model's output at $x$. Use the central finite difference method with a step size of $h = 10^{-3}$.
3. Calculate the sample mean of these calculated derivatives.
4. Compute the 95% bootstrap confidence interval of this mean. Use the percentile method with exactly 1000 bootstrap resamples. To ensure reproducibility, set your random seed to `42` before generating the bootstrap samples (if using Python's NumPy, `np.random.seed(42)`).
5. Build and run an HTTP server listening on `0.0.0.0:8000`. 
6. The server must expose a `GET /stats` endpoint.
7. The endpoint must be protected. It should only return data if the request contains the HTTP header `X-API-Key: model-fitter-88`. Otherwise, return a 401 Unauthorized status code.
8. If authorized, the endpoint must return a JSON response with the following exact keys: `{"mean_derivative": <float>, "ci_95_lower": <float>, "ci_95_upper": <float>}`. Round all float values to 4 decimal places.

Keep the server running in the background or foreground so that it can be tested. You may use any programming language to accomplish this task.