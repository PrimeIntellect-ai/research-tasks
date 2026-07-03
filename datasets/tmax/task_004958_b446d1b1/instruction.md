You are an analyst tasked with processing sensor data and deploying a lightweight statistical API in Go. 

You have been provided with an image containing crucial configuration parameters, located at `/app/config.png`. Use an OCR tool (like `tesseract`) to extract the text from this image. The image contains three key-value pairs:
- `PRIOR_MEAN`: The prior mean for our Bayesian model.
- `PRIOR_VAR`: The prior variance for our Bayesian model.
- `PORT`: The port on which your Go API must listen.

Your task has three phases:

**Phase 1: Data Cleaning (Handling Missing Values and Outliers)**
You have a CSV file at `/home/user/sensor_data.csv` with two columns: `id` and `value`.
1. Read the CSV.
2. Handle missing values: Any row where `value` is empty string or "NaN" should have its value imputed using the **median** of all valid, non-missing `value` entries.
3. Handle outliers: After imputation, drop any rows where the `value` is less than 0.0 or strictly greater than 100.0.

**Phase 2: Bayesian Inference**
Treat the cleaned dataset as a set of observations from a Normal distribution to compute the posterior mean and variance.
Assume the data variance ($\sigma^2$) is the sample variance of your cleaned dataset.
Use the Gaussian conjugate prior update rules:
- Posterior Variance = $1 / (1/\text{PRIOR\_VAR} + N/\sigma^2)$
- Posterior Mean = $\text{Posterior Variance} \times (\text{PRIOR\_MEAN}/\text{PRIOR\_VAR} + (\sum_{i=1}^N x_i) / \sigma^2)$
Where $N$ is the number of cleaned observations and $x_i$ are the cleaned values.

**Phase 3: API Deployment**
Write and run a Go program (e.g., at `/home/user/server.go`) that performs the above data processing on startup and then starts an HTTP server on `0.0.0.0` at the port specified in the image. 

The server must expose the following endpoints:
1. `GET /stats`: Returns a JSON object with the dataset statistics:
   `{"clean_count": <integer>, "sample_variance": <float64>}`
   (Use Bessel's correction, i.e., divide by $N-1$ for sample variance).
2. `GET /posterior`: Returns a JSON object with the Bayesian update results:
   `{"posterior_mean": <float64>, "posterior_variance": <float64>}`

Format your float64 JSON outputs to be reasonably precise (standard Go `json.Marshal` is fine). Leave the server running in the background or foreground so we can query it.