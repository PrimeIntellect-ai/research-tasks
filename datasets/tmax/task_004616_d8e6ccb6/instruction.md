I am a researcher organizing datasets and running Bayesian inference experiments to classify dataset shifts. I have a custom C++ library located in `/app/bayes_infer` that computes the posterior mean of a dataset assuming a Gaussian conjugate prior. However, the library is currently failing to compile.

Here is what I need you to do:
1. **Fix and Build the Library**: Navigate to `/app/bayes_infer` and fix the `Makefile` so that it successfully compiles the library into a shared object `libbayes.so`. There is a deliberate configuration error preventing the creation of the shared library.
2. **Implement an Experiment Tracker Service**: Write a C++ program at `/home/user/tracker.cpp` that links against `libbayes.so`. This program must be a TCP server listening on `127.0.0.1:9000`. 
3. **Handle Requests**: The TCP server should accept incoming connections. Each connection will send a payload consisting of a comma-separated list of decimal numbers (e.g., `1.5,-2.0,3.3`).
4. **Bayesian Inference & Validation**: For each payload, parse the numbers and use the `compute_posterior_mean(const double* data, int size)` function from the `bayes.h` header in `/app/bayes_infer` to calculate the posterior mean. Validate this model output: if the posterior mean is strictly greater than `0.0`, respond to the TCP client with the string `POSITIVE\n`. Otherwise, respond with `NEGATIVE\n`.
5. **Experiment Tracking**: Every time a request is processed, append a line to `/home/user/experiment_log.txt` in the format: `[Data size: N] Posterior Mean: M, Result: R` (where N is the number of elements, M is the mean rounded to 4 decimal places, and R is POSITIVE or NEGATIVE).
6. **Execution**: Compile your `tracker.cpp` and run the service in the background so it is ready to accept requests. Ensure the `LD_LIBRARY_PATH` is set correctly so your executable can find `libbayes.so`.

Please complete the fixes, write the server, and leave the server running on port 9000.