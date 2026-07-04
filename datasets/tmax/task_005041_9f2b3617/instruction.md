You are a data scientist tasked with cleaning a messy sensor dataset and exposing the results via an API for our downstream pipelines. We have received an image containing the specific cleaning parameters and the security token for the API.

Here are your instructions:

1. **Extract Parameters**: Read the image located at `/app/cleaning_instructions.png` using OCR (e.g., `tesseract`). It contains two pieces of information:
   - `Correlation_Threshold=<value>`
   - `Token=<string>`

2. **Clean the Dataset**:
   - Load the raw dataset from `/home/user/sensor_data.csv`.
   - Compute the absolute Pearson correlation matrix for all numerical columns.
   - For any pair of columns that have an absolute correlation strictly greater than the extracted `Correlation_Threshold`, drop the column that appears *later* (further to the right) in the original CSV.
   - Save the cleaned dataset in Parquet format to `/home/user/cleaned_sensor_data.parquet` to optimize large-scale storage reads.

3. **Linear Algebra Analysis**:
   - Compute the covariance matrix of the remaining columns in the cleaned dataset.
   - Calculate the eigenvalues of this covariance matrix.
   - Find the maximum eigenvalue.

4. **Serve the Results**:
   - Build a Python web server (you can use Flask, FastAPI, or the standard library) listening on `127.0.0.1:8080`.
   - Expose a `GET` endpoint at `/api/clean_stats`.
   - The endpoint MUST require an `Authorization` header in the format `Bearer <Token>`, where `<Token>` is the exact token extracted from the image. If the token is missing or incorrect, return an HTTP 401 Unauthorized status.
   - If the token is correct, return an HTTP 200 OK with a JSON payload containing:
     ```json
     {
       "retained_columns": ["col1", "col2", ...],
       "max_eigenvalue": 12.3456
     }
     ```
     *(Note: `max_eigenvalue` should be a float rounded to 4 decimal places).*

Ensure the server is running in the background and is fully completely bound to `127.0.0.1:8080` before you finish the task.