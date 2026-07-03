I need you to build an end-to-end data processing and modeling pipeline that extracts visual features from a laboratory video, joins it with sensor data, trains a tuned predictive model, and serves it via an HTTP API.

Here is your scenario:
We have a video of a chemical reaction experiment located at `/app/experiment_feed.mp4` (24 frames per second, 10 seconds total). We also have two noisy tabular datasets:
1. `/app/sensor_logs.csv` containing timestamps and raw sensor readings (temp, pressure, humidity).
2. `/app/metadata.json` containing experiment offset configurations.

Your tasks:
1. **Video Feature Extraction (ETL):** Extract the frames from `/app/experiment_feed.mp4` using `ffmpeg` or `opencv`. Calculate the average red channel intensity (R from RGB) for each frame. Aggregate this metric to a per-second average.
2. **Data Joining & Cleaning:** Join the aggregated video features (average per-second red intensity) with the sensor logs based on the timestamps. Apply the offset found in `metadata.json` to the sensor timestamps before joining. 
3. **Correlation Analysis:** Perform a correlation analysis on the joined dataset. If any two features have a Pearson correlation coefficient greater than 0.90, drop the one that appears later in the columns list.
4. **Modeling & Tuning:** Train a Ridge Regression model to predict the `target_yield` column. Use 5-fold cross-validation and grid search to tune the `alpha` hyperparameter (search space: 0.1, 1.0, 10.0). Save the best model.
5. **API Deployment:** Create and run a Python web server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`. It must expose a `POST /predict` endpoint that accepts a JSON payload of features, authenticates using a Bearer token `secret-token-123`, and returns a JSON response `{"prediction": <value>}`.

Ensure your server remains running so it can be tested.