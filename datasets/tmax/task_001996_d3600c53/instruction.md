I am a researcher organizing and analyzing my sensor datasets. I need your help to clean the data, find the most important features using a custom high-performance library, train a predictive model, and expose it via a dual-protocol microservice for my team to use.

Here are your instructions:

1. **Fix the Vendored Correlation Package**
   I have a custom Python C-extension for robust correlation located at `/app/fast-corr-py`. Currently, it fails to install via `pip install .` because the `setup.py` is broken (it fails to include the numpy headers correctly). Please fix the `setup.py`, build, and install the package into the current environment so you can `import fast_corr`.

2. **Data Cleaning and Feature Selection**
   Read the dataset at `/home/user/sensor_data.csv`. The target variable is `target`.
   - **Missing Values**: Impute any missing values in the feature columns using the median of that column.
   - **Outliers**: Remove any rows where any feature has a Z-score absolute value strictly greater than 3.0.
   - **Correlation**: Using the `fast_corr.compute(x, y)` function from the package you installed, calculate the correlation of each cleaned feature against the `target`. Select the 2 features with the highest absolute correlation.

3. **Modeling**
   Using only the 2 selected features, train a Ridge Regression model. Use 5-fold cross-validation to tune the `alpha` hyperparameter, searching over the values `[0.1, 1.0, 10.0]`. Keep the model trained on the full cleaned dataset with the best `alpha`.

4. **Serve the Model (Multi-Protocol)**
   Create a single script or application that runs indefinitely and listens on two ports concurrently:
   
   - **HTTP REST API (Port 8080)**:
     Listen on `0.0.0.0:8080`.
     Endpoint: `POST /predict`
     Headers: Must require `Authorization: Bearer research_token`. If missing or incorrect, return a 401 Unauthorized status.
     Request Body: JSON containing the 2 selected features (using their original column names as keys).
     Response Body: JSON format `{"prediction": <predicted_value>}`.
     
   - **TCP Health Service (Port 8081)**:
     Listen on `0.0.0.0:8081` for raw TCP connections.
     When a client sends the string `PING\n` (ending with a newline), the server must reply with `PONG\n` and close the connection.

Please write the server code and start it in the background or leave it running as the final step.