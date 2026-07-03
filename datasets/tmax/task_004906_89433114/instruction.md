I am an ML engineer preparing training data for a new pipeline. We have a multi-service setup where raw event logs are streamed into a Redis cache. Your task is to extract this data, transform it, train a simple regression model, and serve the predictions via a new HTTP service.

Here are the specific requirements:

1. **Start Existing Services:** Run `/app/start_services.sh`. This script will start a local Redis server on `127.0.0.1:6379` and populate a Redis list named `raw_logs` with JSON strings representing user events.
2. **Environment Setup:** You will need to install your own dependencies (e.g., `redis`, `pandas`, `scikit-learn`, `flask`) using `pip`.
3. **Data Transformation & Modeling:** 
   Write a Python script at `/home/user/serve_model.py`. The script must:
   - Connect to the local Redis server.
   - Fetch all items from the list `raw_logs`. Each item is a JSON string resembling `{"user_id": "u123", "action": "view", "count": 5}` or `{"user_id": "u123", "action": "click", "count": 1}`.
   - Aggregate the data to calculate the total `view` count and total `click` count for each `user_id`. (Assume missing actions for a user are 0).
   - Using `scikit-learn`, train a simple `LinearRegression` model where the independent variable (X) is the total `views` and the dependent variable (y) is the total `clicks`.
4. **Service Endpoint:**
   - In the same script, start a Flask application listening on `0.0.0.0:5050`.
   - Provide a GET endpoint at `/predict` that accepts a query parameter `views` (an integer).
   - The endpoint must use the trained model to predict the expected clicks and return a JSON response exactly formatted as: `{"expected_clicks": <float_prediction>}`.

Run your script so the Flask server stays running in the background. Do not stop until the service is actively listening on port 5050.