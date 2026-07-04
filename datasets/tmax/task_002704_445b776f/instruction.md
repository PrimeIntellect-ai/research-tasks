You are a bioinformatics analyst working with a simulated nanopore spectroscopic sequencing pipeline. The data processing pipeline relies on a microservice architecture consisting of Nginx, a Python Flask API, and a Redis datastore. All service files and configurations are located in `/app/`. 

Currently, the pipeline is broken due to configuration mismatches between the services. Your task has two parts:

Part 1: Fix the Pipeline
1. Inspect the configurations in `/app/`. Nginx is configured to serve on port 8080 and proxy to the Flask API. The Flask API fetches pre-computed signal arrays from Redis.
2. Identify and fix the incorrect ports in the Nginx configuration (`/app/nginx.conf`) and the Flask application's environment configuration (`/app/.env` or similar, check the code). 
3. Start the services using the provided `/app/start.sh` script and ensure `http://localhost:8080/data` successfully returns a JSON payload containing a 1D array of signal data under the key `"signal"`.

Part 2: Signal Processing and Parameter Extraction
The signal returned by the API is a noisy electrical current (1D array of 1024 points, sampled at $t = 0, 1, 2, \dots, 1023$). The underlying biophysical signal follows the nonlinear model:
$S(t) = a \cdot e^{-b \cdot t} + c \cdot \sin(d \cdot t)$

Write a Python script to do the following:
1. Fetch the data from `http://localhost:8080/data`.
2. Perform a Fast Fourier Transform (FFT) on the array.
3. Filter out high-frequency noise by zeroing out all FFT coefficients corresponding to frequencies strictly greater than $0.15$ cycles/sample.
4. Perform an Inverse FFT to reconstruct the smoothed real signal.
5. Use a nonlinear equation solver / curve fitting tool (e.g., `scipy.optimize.curve_fit`) on the smoothed signal to fit the model $S(t)$ and extract the parameters. Assume $a \approx 2.0$, $b \approx 0.001$, $c \approx 1.0$, and $d \approx 0.4$ as initial guesses.
6. Extract the fitted periodicity parameter $d$.
7. Save only the numerical value of $d$ (as a standard string, e.g., "0.4201") to `/home/user/periodicity.txt`.

Ensure your Python script is robust and correctly handles the mathematical transformations.