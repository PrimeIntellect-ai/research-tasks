# test_final_state.py
import os
import numpy as np
import pytest

def test_final_model_and_accuracy():
    """
    Verifies that the final_model.pkl exists, is a valid sklearn Pipeline with 
    StandardScaler, PCA, and SVC, and achieves an accuracy >= 0.75 on the test set.
    """
    model_path = "/home/user/final_model.pkl"
    assert os.path.exists(model_path), f"The model file {model_path} does not exist."

    # Import libraries installed by the user
    try:
        import joblib
        import librosa
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.decomposition import PCA
        from sklearn.svm import SVC
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score
    except ImportError as e:
        pytest.fail(f"Failed to import required libraries. Did you install them? Error: {e}")

    # Load the model
    try:
        model = joblib.load(model_path)
    except Exception as e:
        pytest.fail(f"Failed to load the model with joblib. Error: {e}")

    # Verify pipeline structure
    assert isinstance(model, Pipeline), "The saved model is not a sklearn.pipeline.Pipeline."

    step_types = [type(step[1]) for step in model.steps]
    assert StandardScaler in step_types, "Pipeline is missing StandardScaler."
    assert PCA in step_types, "Pipeline is missing PCA."
    assert SVC in step_types, "Pipeline is missing SVC."

    # Verify order: Scaler -> PCA -> SVC
    scaler_idx = step_types.index(StandardScaler)
    pca_idx = step_types.index(PCA)
    svc_idx = step_types.index(SVC)
    assert scaler_idx < pca_idx < svc_idx, "Pipeline steps are in the wrong order. Expected Scaler -> PCA -> SVC."

    # Recreate the dataset
    audio_path = "/app/recording.wav"
    assert os.path.exists(audio_path), f"Audio file missing at {audio_path}"

    y, sr = librosa.load(audio_path, sr=22050)
    chunk_samples = sr * 1
    n_chunks = len(y) // chunk_samples

    X_list = []
    y_labels = []

    for i in range(n_chunks):
        chunk = y[i*chunk_samples : (i+1)*chunk_samples]
        S = np.abs(librosa.stft(chunk))
        X_list.append(S.flatten())
        y_labels.append(1 if np.sum(S) > 500 else 0)

    X = np.array(X_list)
    y_target = np.array(y_labels)

    # Recreate the exact split
    X_train, X_test, y_train, y_test = train_test_split(X, y_target, test_size=0.25, random_state=42)

    # Evaluate the pipeline
    try:
        preds = model.predict(X_test)
    except Exception as e:
        pytest.fail(f"Calling predict() on the pipeline failed. Make sure the pipeline handles raw flattened spectrograms. Error: {e}")

    acc = accuracy_score(y_test, preds)
    assert acc >= 0.75, f"Test accuracy {acc:.4f} is below the threshold of 0.75."

def test_mlflow_tracking():
    """
    Verifies that mlflow was used by checking for the existence of the mlruns directory.
    """
    mlruns_local = os.path.exists("mlruns")
    mlruns_home = os.path.exists("/home/user/mlruns")
    assert mlruns_local or mlruns_home, "MLflow tracking directory 'mlruns' not found. Did you use mlflow to track the experiment?"