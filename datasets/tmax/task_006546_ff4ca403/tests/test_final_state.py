# test_final_state.py
import os

def test_pipeline_script_exists():
    path = "/home/user/pipeline.py"
    assert os.path.isfile(path), f"Expected script {path} does not exist. Did you write the pipeline script?"

def test_best_alpha_file_exists():
    path = "/home/user/best_alpha.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist. Did you execute the pipeline script?"

def test_best_alpha_content():
    path = "/home/user/best_alpha.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    # The expected best alpha is 0.1
    try:
        alpha_val = float(content)
    except ValueError:
        assert False, f"Content of {path} is not a valid float: '{content}'"

    assert alpha_val == 0.1, f"Expected best alpha to be 0.1, but got {alpha_val}. Check your data cleaning and GridSearchCV setup."