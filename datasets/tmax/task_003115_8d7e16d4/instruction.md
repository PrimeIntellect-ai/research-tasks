You are a bioinformatics analyst responsible for processing sequence mutation models. A colleague has digitized an old experimental metadata sheet and saved it as an image at `/app/gel_metadata.png`. You need to extract the model parameters from this image, implement the mathematical model, calculate statistical bounds on a provided dataset, and serve the results via an HTTP API.

Step 1: Information Extraction
Analyze the image at `/app/gel_metadata.png` (using OCR tools like `tesseract` which is installed on the system). It contains three critical pieces of information:
- `AUTH_TOKEN`
- `ALPHA`
- `BETA`

Step 2: Mathematical Modeling and Statistical Analysis
The sequence mutation rate over time $t$ is modeled as $R(t) = \text{ALPHA} \cdot t^{\text{BETA}}$.
You also have a dataset of observed empirical mutation scores in `/app/mutations.csv` (a single column of numbers with the header `score`).
Write a Python application that uses these parameters to perform the following:
1.  **Numerical Integration:** Compute the definite integral of $R(t)$ from $0$ to a given time $t$. 
2.  **Bootstrap Confidence Intervals:** Compute the 95% bootstrap confidence interval for the mean of the scores in `/app/mutations.csv`. You must use 1000 bootstrap resamples and set the random seed to `42` (e.g., `np.random.seed(42)`) before generating the resamples. Calculate the 2.5th and 97.5th percentiles.

Step 3: API Service
Wrap your analysis in an HTTP API using Flask, FastAPI, or Python's standard `http.server`. 
- The server must listen on `127.0.0.1` at port `8000`.
- **Authentication:** Every endpoint must check for the `Authorization` header in the format `Bearer <AUTH_TOKEN>`. If the token is missing or incorrect (does not match the one from the image), return an HTTP 401 Unauthorized status.
- **Endpoint 1:** `GET /integrate?t=<float>` 
  Returns the numerical integral of $R(\tau)$ from $\tau=0$ to $\tau=t$ as JSON: `{"integral": <float_value>}`.
- **Endpoint 2:** `GET /bootstrap`
  Returns the computed 95% bootstrap confidence interval of the mean for the CSV dataset as JSON: `{"ci_lower": <float_value>, "ci_upper": <float_value>}`.

Step 4: Orchestration
Create a shell script at `/home/user/run_server.sh` that installs any necessary Python dependencies (like `flask`, `scipy`, `pandas` - assuming standard pip availability) and starts your API server in the background. Ensure the script is executable.