# test_final_state.py

import os

def test_process_data_script_exists():
    path = "/home/user/process_data.py"
    assert os.path.isfile(path), f"The script {path} does not exist."

def test_dataset_rp_exists():
    path = "/home/user/dataset.rp"
    assert os.path.isfile(path), f"The final output file {path} does not exist. Did the pipeline run successfully?"

def test_dataset_rp_file_size():
    path = "/home/user/dataset.rp"
    assert os.path.isfile(path), f"File {path} does not exist."

    size = os.path.getsize(path)
    threshold = 8000000

    assert size <= threshold, (
        f"File size of {path} is {size} bytes, which exceeds the threshold of {threshold} bytes. "
        "This indicates that the compression bug in `research_packer` was not properly fixed."
    )