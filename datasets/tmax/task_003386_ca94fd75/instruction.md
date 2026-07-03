You are tasked with fixing and completing a data science pipeline that processes experimental results and exposes the analyzed data via an API.

You have been provided an image at `/app/api_spec.png` which contains notes from the lead engineer regarding the API specifications. You must extract the required port, the endpoint path, the required authentication token, and the response format from this image.

The raw data is located in:
1. `/home/user/data/records.csv`: Contains experiment results with columns `id`, `trials`, `successes`, and `source_id`.
2. `/home/user/data/reference.json`: Contains Bayesian prior parameters (`alpha` and `beta`) mapped to each `source_id`.

Your objectives:
1. Parse the API requirements from `/app/api_spec.png`.
2. Build an ETL pipeline to join the CSV records with the corresponding priors from the JSON file based on `source_id`.
3. For each record, perform Bayesian inference to calculate the posterior mean of the success rate using a standard Beta-Binomial conjugate model.
4. Write a script that serves this data via an HTTP API.
5. The API must listen on the IP `127.0.0.1` and the exact port specified in the image.
6. The API must expose the endpoint path specified in the image. It should accept an `id` as a query parameter (e.g., `?id=1`).
7. The API must enforce authentication by checking the `Authorization` header for the exact token specified in the image. If unauthorized, return HTTP 401. If the `id` does not exist, return HTTP 404.
8. If successful, the API must return an HTTP 200 response with the JSON format strictly matching the one specified in the image.

Ensure the server runs in the background or use a multiplexer so it stays active. The automated verifier will issue real HTTP requests to your service to validate the data, calculations, and API compliance.