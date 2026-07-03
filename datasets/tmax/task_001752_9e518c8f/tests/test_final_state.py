# test_final_state.py
import os
import re
import requests
import pytest

def test_makefile_fixed():
    makefile_path = "/app/text_prep_serve/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "requirements.txt" in content, "Makefile was not fixed to use 'requirements.txt'"
    assert "requirments.txt" not in content, "Makefile still contains the typo 'requirments.txt'"

def test_prepare_script_fixed():
    prepare_path = "/app/text_prep_serve/src/prepare.py"
    assert os.path.isfile(prepare_path), "prepare.py is missing"
    with open(prepare_path, "r") as f:
        content = f.read()

    # The fix should ensure fit_transform is only called on the train split
    # and transform is called on the test split.
    assert re.search(r"fit_transform\s*\(.*train", content, re.IGNORECASE) or \
           "fit_transform" in content and "transform" in content, \
           "prepare.py does not seem to properly separate fit_transform for train and transform for test"

def test_models_generated():
    models_dir = "/app/text_prep_serve/models"
    assert os.path.isdir(models_dir), f"{models_dir} directory is missing"
    files = os.listdir(models_dir)
    assert len(files) > 0, "No models or vectorizer found in the models directory"

def test_api_server_predict():
    url = "http://127.0.0.1:8000/predict"
    payload = {"text": "unseen test document with rare words"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "prediction" in data, "Response JSON missing 'prediction' key"
    assert isinstance(data["prediction"], int), "Prediction must be an integer"