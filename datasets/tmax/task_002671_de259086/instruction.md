You are a Data Engineer building an automated ETL and analytics pipeline for an IoT sensor network. Due to a legacy system constraint, some field sensors transmit their daily logs as synthesized speech in an audio file.

Your task is to build a Python-based ETL pipeline that transcribes the audio, extracts the measurements, performs statistical and Bayesian analysis, and exposes the results via a REST API.

**Step 1: Extraction & Transformation**
1. You are provided with an audio file at `/app/data/telemetry_audio.wav`. It contains a sequence of spoken sensor readings for two sensors: "Alpha" and "Beta".
2. Transcribe this audio file using any suitable local speech-to-text library (e.g., `SpeechRecognition`, `whisper`, `vosk`).
3. Parse the transcript to extract the numerical values for "Alpha" and "Beta". Assume the readings are interleaved (e.g., Alpha reading, then Beta reading, and so on).

**Step 2: Statistical Modeling & Inference**
Using the extracted arrays of values for Alpha and Beta, compute the following:
1. **Hypothesis Testing**: Perform an independent two-sample t-test (Welch's t-test, assuming unequal variances) to check if the mean of Alpha is significantly different from the mean of Beta. Extract the p-value.
2. **Bayesian Inference**: Estimate the posterior mean and 95% credible interval for the true mean of sensor **Alpha**.
   - Assume the data likelihood for Alpha is Normally distributed with a known variance $\sigma^2 = 1.0$.
   - Use a Normal conjugate prior for the mean of Alpha with prior mean $\mu_0 = 20.0$ and prior variance $\sigma_0^2 = 25.0$.
   - Calculate the analytical posterior mean and the lower/upper bounds of the 95% credible interval (using the 2.5th and 97.5th percentiles of the posterior normal distribution).

**Step 3: Serving the Results**
Create a Python web service (using Flask, FastAPI, or similar) that listens on `127.0.0.1:8080`.
The service must expose a `GET /metrics` endpoint that returns a JSON response with exactly the following keys and structure:

```json
{
  "alpha_values": [/* list of floats */],
  "beta_values": [/* list of floats */],
  "t_test_p_value": /* float */,
  "bayesian_posterior_mean": /* float */,
  "bayesian_ci_lower": /* float */,
  "bayesian_ci_upper": /* float */
}
```

**Constraints:**
- You must write the necessary scripts and leave the web service running in the background.
- Round all float outputs in the JSON to 3 decimal places.
- Ensure the API returns a 200 OK status code.
- You can install any required Python packages (e.g., `scipy`, `fastapi`, `uvicorn`, `SpeechRecognition`).