I need you to build an end-to-end data cleaning and serving pipeline for a multi-lingual dataset I am working on. We have a dirty dataset and a scanned reference image, and we need to clean the data, impute missing values, and serve the results via a local HTTP API.

Here are the components you have to work with:
1. **/app/dirty_corpus.csv**: A CSV file with columns `id`, `text_entry`, `value_a`, and `value_b`. 
2. **/app/reference_key.png**: An image of a printed note that contains a critical numeric multiplier for our data (e.g., "MULTIPLIER: X.XX").

Here is the exact workflow you must implement in Python:

**Step 1: OCR & Extraction**
Extract the text from `/app/reference_key.png` (using tesseract) and parse out the floating-point multiplier value. 

**Step 2: Data Cleaning & Interpolation**
Read `/app/dirty_corpus.csv` and process it:
*   `text_entry`: This column contains messy multi-lingual text with inconsistent Unicode formats, emojis, and punctuation. You must write a function to normalize the text using Unicode NFKC, remove all characters that are not letters, numbers, or whitespace, lowercase the string, and then tokenize it by splitting on whitespace. **Requirement:** You must process these text entries in parallel (using `multiprocessing` or `concurrent.futures`) to simulate processing a massive dataset.
*   `value_a`: This column has missing values (empty strings). You must impute these missing values using standard linear interpolation based on the row order (sorted by `id`).
*   `value_b`: Multiply every value in this column by the multiplier extracted from the image in Step 1.

**Step 3: Serve the Data (API)**
Instead of writing to a file, you must serve the cleaned data via a local REST API. 
Write a Python server (using Flask, FastAPI, or the standard `http.server`) that listens on `127.0.0.1:8000`.
*   **Endpoint:** `GET /api/v1/record/<id>`
*   **Authentication:** The endpoint must require an `Authorization` header with the exact value `Bearer ds_secret_2024`. If missing or incorrect, return a 401 status code.
*   **Response:** If the `id` exists, return a 200 OK status with a JSON payload strictly in this format:
    `{"id": <int>, "tokens": ["list", "of", "words"], "imputed_a": <float>, "scaled_b": <float>}`
    *(Note: Ensure floats are rounded to 2 decimal places if necessary, but standard Python floating point representation is fine as long as the math is correct).*
    If the `id` does not exist, return a 404 status.

Please start the server and leave it running in the background or foreground so my automated test suite can query it.