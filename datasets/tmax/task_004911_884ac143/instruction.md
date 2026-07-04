You are acting as a Capacity Planner for our internal cloud infrastructure. We need to deploy a robust, automated pipeline to forecast resource usage for the next 30 days based on historical data and infrastructure constraints.

Your task has several components:

1. **Environment & CI/CD Pipeline Setup:**
   Create a robust shell script at `/home/user/planner/deploy.sh` that:
   - Sets up a local Python virtual environment in `/home/user/planner/venv`.
   - Sets necessary environment variables (e.g., `PLANNER_ENV=production`).
   - Installs any required Python packages (e.g., pandas, scikit-learn, pytesseract, Pillow).
   - Includes robust error handling (fails if any step fails).
   - Executes your forecasting Python script.

2. **Information Extraction:**
   There is a dashboard screenshot located at `/app/dashboard_multipliers.png`. This image contains crucial capacity planning parameters (specifically, an overarching system "Growth Factor" and a "Weekend Discount" percentage). You must write code to extract these parameters (using OCR or vision processing) and incorporate them into your forecasting logic.

3. **Forecasting Implementation:**
   Write a Python script at `/home/user/planner/forecast.py` that:
   - Reads historical daily CPU usage data from `/home/user/planner/data/history.csv` (contains columns `day` and `cpu_load` for days 1 to 100).
   - Fits a trend model to the historical data.
   - Adjusts the forecast using the "Growth Factor" and "Weekend Discount" extracted from the image. (Assume the historical data already inherently includes weekend patterns, but future data from day 101 onwards must strictly apply the exact Growth Factor multiplier to the baseline trend, and the Weekend Discount to days that are multiples of 7 plus 6 or 0, e.g., assuming day 1 was a Monday).
   - Outputs the predictions for days 101 to 130 to `/home/user/planner/output/forecast.csv`. The output CSV must have two columns: `day` and `predicted_load`.

To complete the task, your predictions must closely match our hidden baseline. The automated verifier will calculate the Mean Squared Error (MSE) between your `forecast.csv` and the true underlying mathematical model of the future usage. Your MSE must be strictly less than 2.0.

Ensure all directories exist and permissions are correct before running your pipeline.