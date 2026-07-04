A researcher is organizing a dataset derived from an audio recording and building a classification model, but their current pipeline is overestimating performance due to data leakage. 

You have been provided with an audio file at `/app/recording.wav` and a starter script at `/home/user/pipeline.py`. The script is supposed to:
1. Load the audio file and slice it into 1-second chunks.
2. Extract the magnitude spectrogram for each chunk.
3. Flatten the spectrograms to create a feature matrix `X`.
4. Generate synthetic labels `y` based on the total energy of each chunk (already implemented).
5. Apply Standard Scaling and Principal Component Analysis (PCA) to reduce the dimensionality.
6. Train a Support Vector Classifier (SVC).

However, the researcher accidentally introduced data leakage by applying `fit_transform` for the scaler and PCA on the *entire* dataset `X` before splitting it into training and testing sets. 

Your task is to:
1. Set up your Python environment by installing `librosa`, `scikit-learn`, `numpy`, and `mlflow`.
2. Fix the data leakage in `/home/user/pipeline.py`. You must rewrite the preprocessing and modeling steps to properly use a `sklearn.pipeline.Pipeline`. The Scaler and PCA must only be fitted on the training data.
3. Set up local experiment tracking using `mlflow`. Log the PCA `n_components` parameter and the correct `test_accuracy` metric.
4. Tune the pipeline (e.g., number of PCA components, SVC hyperparameters) so that the properly evaluated test accuracy is at least 0.75. 
5. Save your trained `Pipeline` object (which must include the scaler, PCA, and SVC) to `/home/user/final_model.pkl` using `joblib`.

Do not change the random seed (use `random_state=42`) or the logic that generates the synthetic labels `y`. The train/test split should use `test_size=0.25`, `random_state=42`.