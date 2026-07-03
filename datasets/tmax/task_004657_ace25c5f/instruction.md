You are tasked with deploying a specialized model-fitting service for a spectroscopy laboratory. 

We have a proprietary signal generation engine provided as a stripped binary located at `/app/signal_gen`. This binary acts as an oracle for our physical system. It takes three command-line arguments (Amplitude, Decay Time, Frequency) and outputs a comma-separated list of 100 signal intensity values representing a simulated time-domain spectroscopy signal (Free Induction Decay).

Your objective is to write a Python-based HTTP web service that performs parameter inference on noisy experimental data. 

Requirements:
1. Analyze the `/app/signal_gen` binary by treating it as a black box (or using reverse engineering tools) to understand how the three inputs map to the output signal. 
2. Create a Python web service that listens on `127.0.0.1:8080`.
3. The service must expose an HTTP POST endpoint at `/fit`.
4. The `/fit` endpoint will receive a JSON payload containing noisy spectroscopic data in the format: `{"data": [val1, val2, ..., val100]}`.
5. Upon receiving the data, your service must use curve fitting, MCMC sampling, or Monte Carlo optimization to find the best-fit parameters (Amplitude, Decay Time, Frequency) that would cause `/app/signal_gen` to produce a signal matching the provided noisy data as closely as possible (minimizing the sum of squared errors).
6. Be careful: standard numerical integration or fitting methods might diverge if the parameter bounds are not appropriately constrained (e.g., negative decay times).
7. The endpoint must return a JSON response containing the fitted parameters: `{"amplitude": A, "decay": D, "frequency": F}`.
8. The service must authenticate requests by checking for the HTTP header `Authorization: Bearer LabSecret99`. Return a 401 Unauthorized status if this header is missing or incorrect.

Please write the Python code for this service, ensure all necessary dependencies (like `scipy`, `numpy`, `flask` or `fastapi`) are installed, and start the service in the background so it is ready to receive requests.