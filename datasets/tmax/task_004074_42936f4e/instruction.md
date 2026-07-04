You are a bioinformatics analyst tasked with processing raw nanopore sequencing signals. Our lab has a multi-service pipeline simulating a sequencer and an evaluation backend, but the raw electrical signals need to be properly calibrated (scaled and shifted) to match the expected statistical distribution (density estimation) of our reference genome.

Under `/app/`, there are two unconfigured services that you need to start and orchestrate:
1. **Sequencer API (`/app/sequencer.py`)**: A service simulating the nanopore signal stream. It runs on port `5000`. You can retrieve a raw signal array by sending a `GET` request to `http://localhost:5000/signal`.
2. **Scorer API (`/app/scorer.py`)**: A scoring backend running on port `5001`. It evaluates how well a calibrated signal matches the expected density distribution. You can `POST` to `http://localhost:5001/score` with a JSON payload: `{"signal": [list_of_raw_floats], "scale": float, "shift": float}`. It responds with a JSON object containing the `mse` (Mean Squared Error) between the calibrated signal's kernel density estimate and the expected biological profile.

Your tasks are:
1. Inspect the services in `/app/` and figure out how to start them. The sequencer API might require a specific environment variable to bind to the correct port, and the scorer needs Redis to cache profiles (Redis is already installed but must be started on the default port).
2. Write a pure **Bash** script at `/home/user/calibrate.sh` that acts as the orchestrator and optimizer.
3. Your script must fetch a signal from the sequencer, and then use an optimization technique (e.g., grid search, gradient descent, or a randomized search written in bash using `curl` and `awk`/`bc`) to find the optimal `scale` and `shift` values.
   - The valid range for `scale` is between 0.1 and 3.0.
   - The valid range for `shift` is between -5.0 and 5.0.
4. Minimize the `mse` returned by the Scorer API.
5. Save the best parameters to a file exactly at `/home/user/calibration_result.txt` in the following format:
```
scale=<float>
shift=<float>
mse=<float>
```

To succeed, the final `mse` evaluated on your parameters must be strictly less than **0.02**. Make sure your bash script is executable and runs autonomously.