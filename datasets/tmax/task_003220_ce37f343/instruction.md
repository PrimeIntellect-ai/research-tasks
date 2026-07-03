You are an analyst tasked with building a mathematical modeling API based on provided CSV datasets and a specification image. 

Your environment contains the following files:
1. `/app/data/features.csv`: Contains `customer_id`, `x1`, `x2`, `x3`.
2. `/app/data/targets.csv`: Contains `customer_id`, `y`.
3. `/app/data/specs.png`: An image containing a snippet of text that specifies the statistical significance level (`ALPHA`) required for hypothesis testing.

Your task:
1. **Data Joining**: Join the two CSV files on `customer_id`. Sort the data by `customer_id` ascending.
2. **OCR Extraction**: Use OCR (e.g., `pytesseract`) to read `/app/data/specs.png` and extract the numerical value of `ALPHA`.
3. **Model Training & Linear Algebra**: Fit an Ordinary Least Squares (OLS) regression model to predict `y` using `x1`, `x2`, and `x3`. You must include an intercept term (as the first feature column). 
4. **Hypothesis Testing / CIs**: Compute the Confidence Intervals for the regression coefficients (intercept, x1, x2, x3) using the `ALPHA` value extracted from the image. Use the standard t-distribution critical values for the confidence intervals.
5. **API Deployment**: Create and run an HTTP REST service using Python (e.g., FastAPI or Flask) listening on `127.0.0.1:8000`.

The API must expose the following two endpoints:
- `POST /predict`: Accepts a JSON payload `{"x1": float, "x2": float, "x3": float}` and returns `{"prediction": float}` representing the predicted `y` value.
- `GET /ci`: Returns the confidence intervals for the coefficients as a JSON object:
  ```json
  {
    "intercept": [lower_bound, upper_bound],
    "x1": [lower_bound, upper_bound],
    "x2": [lower_bound, upper_bound],
    "x3": [lower_bound, upper_bound]
  }
  ```

Start your server as a background process or leave it running in the foreground so it can be queried. The automated test will send HTTP requests to verify the correctness of your math and modeling.