You are a Data Engineer tasked with completing an automated ETL pipeline that computes the Pearson correlation of features and serves the result via an API.

There is a dataset located at `/app/dataset.csv` containing columns: `id`, `featureA`, `featureB`, and `split`. We recently discovered a data leak in our previous pipeline where test data was included in the training correlation calculation. 

Your tasks are:
1. Construct a reproducible pipeline (using your choice of tools/languages) to calculate the Pearson correlation coefficient between `featureA` and `featureB`, but **only** for rows where the `split` column is exactly `train`.
2. Extract the secret API token from an image artefact located at `/app/auth_token.png`. This image contains a single line of text which is our internal API token. You may use `tesseract` to read this.
3. Start an HTTP server listening on `127.0.0.1:8000`. 
4. Expose a single endpoint: `GET /api/v1/correlation`.
5. This endpoint MUST require an `Authorization` header in the format `Bearer <TOKEN>`, where `<TOKEN>` is the text extracted from the image (stripped of any trailing whitespace/newlines).
6. If the token is missing or incorrect, return a `401 Unauthorized` status.
7. If the token is correct, return a `200 OK` status with a JSON response in the exact format: `{"correlation": <value>}`, where `<value>` is the calculated Pearson correlation rounded to 4 decimal places (e.g., 0.1234).
8. Keep the server running in the background so that our automated test suite can verify it. 

Ensure your server is robust and handles the required route and authentication properly.