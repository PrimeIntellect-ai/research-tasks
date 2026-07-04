You are an MLOps engineer tasked with building a reproducible experiment tracking pipeline using Bash, and exposing it via a network service.

We have a dashboard camera video located at `/app/dashcam.mp4`. We want to run a simple probabilistic model to determine the likelihood that the vehicle is driving in a "Sunny" environment (State=1) versus "Overcast" (State=0). 

Your task is to build a two-part system:

**1. The Reproducible Bash Pipeline (`/home/user/pipeline.sh`)**
Write a bash script that takes two arguments: a `prior` probability (e.g., 0.5) and a brightness `threshold` (integer 0-255).
The script must perform the following:
* Extract all frames from `/app/dashcam.mp4` at 1 frame per second using `ffmpeg` into a temporary directory.
* For each extracted frame (in order of time), calculate its average grayscale brightness (0-255). You can use ImageMagick (`convert -colorspace gray -format "%[fx:mean*255]" info:`) or any other CLI tool.
* Perform a sequential Bayesian update. Let P(S=1) be the `prior` initially.
  * If the frame's brightness is `>= threshold`, we observe Evidence=1. Otherwise, Evidence=0.
  * The likelihoods are known: 
    * P(Evidence=1 | S=1) = 0.85
    * P(Evidence=0 | S=1) = 0.15
    * P(Evidence=1 | S=0) = 0.40
    * P(Evidence=0 | S=0) = 0.60
  * Use Bayes' theorem to update P(S=1) after each frame.
* **Experiment Tracking:** The script must create a tracking directory `/home/user/experiments/run_<timestamp>_prior_<prior>_thresh_<threshold>/`. Inside this directory, save:
  * `config.txt` containing the prior and threshold.
  * `trace.csv` containing the frame index, calculated brightness, Evidence (0 or 1), and the updated P(S=1) (up to 4 decimal places) for each frame.
* The script should output ONLY the final posterior probability P(S=1) to `stdout` (e.g., `0.9231`).

**2. The Inference Service**
Create an HTTP server (you may use Python, Flask, or FastAPI for this component, but it MUST invoke your `pipeline.sh` for the actual logic).
* The server must listen on `0.0.0.0:8080`.
* It must expose a `GET /infer` endpoint that accepts query parameters `prior` and `threshold`.
* The endpoint must require an `Authorization` header containing exactly: `Bearer mlops-track-99`. Requests without this or with a wrong token should return a 401 Unauthorized status.
* When a valid request is received, the server should execute `/home/user/pipeline.sh <prior> <threshold>`, capture its output (the final probability), and return a JSON response: `{"final_probability": <value>}`.

Ensure your service is running in the background before you finish the task. Do not stop the service.