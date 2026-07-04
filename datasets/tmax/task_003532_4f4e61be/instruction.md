You are a data analyst at a manufacturing company. You've been given a dataset of sensor readings and a scanned sticky note from the lead engineer containing critical configuration parameters.

Your task is to build a multi-language pipeline to analyze this data and expose the results via an HTTP API.

1. **Extract Configuration from Image:**
   There is a scanned note located at `/app/config_scan.png`. Use an OCR tool (like `tesseract`, which is preinstalled) to extract the text. The note contains two key pieces of information:
   - An API authentication token.
   - The significance level ($\alpha$) to be used for all statistical confidence intervals.

2. **Statistical Analysis (R):**
   The sensor data is located at `/app/sensor_data.csv`. 
   Write an R script to compute statistical metrics between any two columns of this dataset. The script must compute:
   - The sample covariance.
   - The Pearson correlation coefficient.
   - The confidence interval of the correlation coefficient, using the exact $\alpha$ extracted from the image.
   *Hint: R's `cor.test()` computes confidence intervals for correlations.*

3. **API Server (Python):**
   Create a Python HTTP web server (e.g., using Flask or FastAPI) that exposes these R-based calculations.
   - The server must listen on exactly `127.0.0.1:9090`.
   - Provide a GET endpoint at `/api/v1/stats`.
   - The endpoint must accept two query parameters: `var1` and `var2` (representing column names from the CSV).
   - The endpoint must enforce authentication. It must require an `Authorization` header in the format `Bearer <TOKEN>`, where `<TOKEN>` is the exact token extracted from the image. Return a 401 status code if missing or incorrect.
   - The response must be a JSON object with exactly the following keys and float values (rounded to 4 decimal places):
     ```json
     {
       "covariance": <float>,
       "correlation": <float>,
       "ci_lower": <float>,
       "ci_upper": <float>
     }
     ```

Run your server in the background so it is available for testing. Do not exit your final terminal session until the server is running on port 9090.