You are a data scientist tasked with cleaning a dataset, extracting features, and tracking your model training using a local MLflow setup.

Part 1: Fix the Experiment Tracking Infrastructure
We have a multi-service experiment tracking stack located at `/app/docker-compose.yml`. It consists of PostgreSQL (backend store), MinIO (artifact store), and MLflow. 
Currently, the MLflow service fails to start because of misconfigurations in the `docker-compose.yml` file (specifically, the `MLFLOW_BACKEND_STORE_URI` is pointing to the wrong database port, and the MinIO credentials/URL are incorrect). 
1. Fix the configuration in `/app/docker-compose.yml` so that MLflow can successfully connect to Postgres and MinIO.
2. Bring up the services using `docker-compose up -d`. Make sure MLflow is accessible at `http://localhost:5000`.

Part 2: Data Cleaning and Feature Engineering
You have a raw dataset at `/home/user/train_data.csv`. The target variable is `target`. The other columns are numerical features `f0` to `f49`.
1. The dataset contains missing values (`NaN`). Impute these missing values using the mean of each column.
2. The features are highly collinear. Use Principal Component Analysis (PCA) to reduce the feature space to exactly 10 components. (Do not scale the features before PCA for this specific task).
3. Train a Ridge Regression model (`sklearn.linear_model.Ridge`) with `alpha=1.0` on the engineered features.

Part 3: Experiment Tracking and Delivery
1. Log your training run to the MLflow server at `http://localhost:5000`. Create an experiment named `Feature_Engineering_Exp` and log the Mean Squared Error (MSE) on your training data.
2. Save your complete modeling pipeline (Imputer -> PCA -> Ridge) as a single scikit-learn Pipeline object using `joblib` to `/home/user/model.pkl`.

An automated verifier will load `/home/user/model.pkl` and evaluate its R^2 score on a hidden test dataset.