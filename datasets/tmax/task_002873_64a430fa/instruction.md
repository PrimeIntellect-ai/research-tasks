You are an AI assistant helping a data science researcher organize and analyze a new audio dataset. 

The researcher has received a new audio sample located at `/app/dataset.wav`. To integrate this into our probabilistic modeling pipeline, we need a small microservice written in Go that extracts features from this audio file, performs basic statistical and Bayesian analysis, and serves the results over HTTP.

Please create a Go HTTP server that listens on `127.0.0.1:8080`. The server must expose a single endpoint: `GET /metrics`.

When the `/metrics` endpoint is called, the server should:
1. **Extract Audio Duration**: Dynamically determine the duration (in seconds) of the `/app/dataset.wav` file. You may shell out to `ffprobe` to get this value.
2. **Hypothesis Testing (Z-Score)**: We have a historical baseline distribution for audio durations modeled as a Normal distribution with mean $\mu_0 = 10.0$ and variance $\sigma_0^2 = 4.0$ (standard deviation = 2.0). Calculate the Z-score for the extracted duration against this baseline.
3. **Bayesian Inference**: Treat the extracted duration as a single observation $x$ with a known observation variance $\sigma^2 = 1.0$. Calculate the Bayesian posterior mean for the duration. The formula for the posterior mean of a Normal distribution given a Normal prior is:
   `posterior_mean = (mu0/sigma0_sq + x/sigma_sq) / (1/sigma0_sq + 1/sigma_sq)`
4. **Reproducibility Check**: To ensure pipeline reproducibility, the server must extract the duration a second time and assert that the two extracted values are identical. If they are not, the server should return an HTTP 500 error.

If the reproducibility check passes, the endpoint must return a JSON response with exactly the following structure (using floating-point numbers):
```json
{
  "duration": 5.23,
  "z_score": -2.385,
  "posterior_mean": 6.184
}
```
*(The values above are just examples).*

**Constraints:**
- Write your code in a file named `/home/user/server.go`.
- Run the server in the background so it stays active.
- Ensure the server is listening on `127.0.0.1:8080` before finishing.
- You can use standard standard Linux tools like `ffprobe` (from the `ffmpeg` package) to parse the audio.