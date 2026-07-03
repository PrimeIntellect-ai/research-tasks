You are a data analyst tasked with predicting chemical reaction yields from a combination of tabular sensor data and video feed analysis. 

We have an experiment video located at `/app/reaction_experiment.mp4` recorded at 1 frame per second. Alongside it, we have training sensor data logged at `/home/user/train_log.csv` and testing sensor data logged at `/home/user/test_log.csv`. The CSVs record the timestamp (`time_sec`), the reactor `temperature`, and a binary indicator `catalyst` (whether the catalyst is active). 

The target variable is `reaction_yield`, which is provided in the training set but missing from the test set. The visual color of the reaction in the video (specifically, the intensity of the red channel) is a known strong predictor of the yield when combined with the tabular sensor data.

Your task is to:
1. Extract the frames from `/app/reaction_experiment.mp4`.
2. Process the frames to extract visual features (e.g., the mean red-channel pixel value for each second/frame).
3. Merge these engineered visual features with the provided tabular data using the time sequence (Frame 0 corresponds to `time_sec = 0`, Frame 1 to `time_sec = 1`, etc.).
4. Train a regression model (using any framework of your choice, such as scikit-learn) on the training set to predict `reaction_yield`.
5. Apply your model to the test set (`/home/user/test_log.csv`) combined with the corresponding video features.
6. Generate your final predictions and save them to a file named exactly `/home/user/predictions.csv`.

The output file `/home/user/predictions.csv` must contain exactly two columns: `time_sec` and `predicted_yield`, formatted as a standard comma-separated values file with a header.

Your success will be measured by the Root Mean Squared Error (RMSE) of your predictions against the hidden ground truth for the test set. You must achieve an RMSE of less than 4.0 to pass.

You may use any programming language or shell tools to complete this workflow.