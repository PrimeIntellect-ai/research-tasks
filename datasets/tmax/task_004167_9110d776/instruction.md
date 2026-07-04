I need you to fix a data preparation and modeling pipeline written in Rust. We have a vendored package located at `/app/linreg_pipeline` that joins two data sources (`/app/data/features.csv` and `/app/data/targets.csv`), processes them, and trains a basic linear regression model to predict a target variable.

Currently, the model's performance is terrible. I suspect there is a subtle bug in how the data joining or parsing is handled—specifically around missing values in an integer feature column. When missing values occur, the pipeline might be silently converting them to zeros or causing silent precision loss, which ruins the linear regression model.

Your task is to:
1. Inspect the Rust project in `/app/linreg_pipeline`.
2. Identify and fix the data parsing/joining bug so that missing values in the integer column are properly handled (you should drop rows with missing values instead of letting them default to 0).
3. Build and run the pipeline to generate the predictions file at `/app/linreg_pipeline/predictions.csv`.

The output `/app/linreg_pipeline/predictions.csv` must contain the test set predictions. Our automated verification will compute the Mean Squared Error (MSE) between your predictions and the true targets. You must achieve an MSE of 0.5 or lower to pass.