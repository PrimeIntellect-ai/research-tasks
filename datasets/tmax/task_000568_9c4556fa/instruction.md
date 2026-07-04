You are an expert data scientist and systems engineer. We have a data pipeline that processes tabular data. Sometimes, the data ingestion system silently introduces missing values (nulls) into integer columns, forcing them into floats (a common issue similar to pandas NaN introduction). 

We need a robust, automated Rust-based data cleaning microservice to fix this on the fly. 

First, there is an image file located at `/app/schema_rules.png`. You need to use OCR (e.g., `tesseract`) to read the instructions from this image. It contains the required parameters for the imputation rule and the confidence interval.

Your task is to create a Rust web service that does the following:
1. Listens on `127.0.0.1:9090`.
2. Exposes a `POST` endpoint at `/clean`.
3. The endpoint will receive a JSON payload with a "data" array of objects containing two numeric columns: "A" and "B". Some values in column "B" will be `null`.
   Example payload:
   `{"data": [{"A": 1.0, "B": 2.0}, {"A": 2.0, "B": null}, {"A": 3.0, "B": 6.0}]}`
4. For the missing values in "B", you must impute them using simple 1-dimensional linear regression, modeling "B" as a function of "A" ($B = \beta_0 + \beta_1 A$). Fit the regression line ONLY on the rows where "B" is not null. Then use the fitted line to predict the missing "B" values based on their "A" values.
5. After imputing all missing values, calculate the 95% confidence interval for the mean of the complete column "B". Use the Normal approximation ($Z$-score) specified in the image, and use the sample standard deviation (denominator $n-1$).
6. The service must return a JSON response with the imputed column "B" as an array of floats, and the lower and upper bounds of the confidence interval.
   Expected response format:
   `{"imputed_B": [2.0, 4.0, 6.0], "ci_lower": 1.7368, "ci_upper": 6.2632}`
   (Round the outputs to 4 decimal places if necessary).

You must write, compile, and run this service in the background so it is actively listening on port 9090 when you finish the task. You are free to use any Rust crates you like (e.g., `axum`, `actix-web`, `serde`, etc.). Create the project in `/home/user/cleaner_service`.