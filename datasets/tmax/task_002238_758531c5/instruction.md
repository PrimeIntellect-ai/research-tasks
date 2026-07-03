You are a Data Scientist and Go developer working on a legacy machine learning pipeline. 

We have a proprietary legacy data-cleaning oracle binary located at `/app/clean_oracle`. This binary is stripped, and we don't have its source code. It reads comma-separated raw features from standard input (3 columns: `f1`, `f2`, `f3`) and outputs cleaned comma-separated features to standard output (3 columns).

We also have a raw training dataset at `/home/user/data/train.csv` with 4 columns: `f1, f2, f3, target`.

Your task involves several stages:

1. **Data Cleaning & Analysis Environment:**
   Process the first 3 columns of `/home/user/data/train.csv` through the `/app/clean_oracle` to generate a cleaned training dataset. 

2. **Model Training & Hyperparameter Tuning in Go:**
   Write a Go program using the `gonum.org/v1/gonum` library to train a Ridge Regression model. Your model must predict the `target` variable using the 3 *cleaned* features. 
   You must implement a 3-fold Cross-Validation routine to select the optimal L2 regularization penalty ($\lambda$) from the candidate set: `{0.1, 1.0, 10.0}`. Evaluate folds using Mean Squared Error (MSE). The folds should be split sequentially (i.e., first 33% is fold 1, next 33% is fold 2, last 34% is fold 3). 

3. **Multi-Protocol Serving API:**
   Once you have identified the optimal $\lambda$ and trained the final model on the *entire* dataset using that $\lambda$, wrap your model in a Go-based web service. 
   The service must handle raw feature inputs, clean them dynamically (either by wrapping `/app/clean_oracle` via `os/exec` or by reverse-engineering its logic), apply the trained model weights, and return the prediction.

   The service must expose two endpoints concurrently:
   - **HTTP API:** 
     Listen on `0.0.0.0:8080`.
     Endpoint: `POST /predict`
     Accepts JSON: `{"f1": 1.2, "f2": 3.4, "f3": 5.6}`
     Returns JSON: `{"prediction": 12.345}`
   - **gRPC API:**
     Listen on `0.0.0.0:50051`.
     Implement the gRPC service defined in `/home/user/predictor.proto`. You will need to compile the protobuf file and implement the server.

Leave the service running in the foreground so it can be tested. Ensure your Go module is initialized in `/home/user/app` and all dependencies are properly fetched.