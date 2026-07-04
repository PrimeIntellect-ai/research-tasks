# test_final_state.py
import os
import json
import stat

def test_run_pipeline_exists_and_executable():
    file_path = '/home/user/run_pipeline.sh'
    assert os.path.exists(file_path), f"The script {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{file_path} is not executable."

def test_run_pipeline_uses_jq():
    file_path = '/home/user/run_pipeline.sh'
    assert os.path.exists(file_path), f"The script {file_path} is missing."
    with open(file_path, 'r') as f:
        content = f.read()
    assert 'jq' in content, f"The script {file_path} does not use 'jq' as required."

def test_analysis_results_json():
    file_path = '/home/user/analysis_results.json'
    assert os.path.exists(file_path), f"The output file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} is not valid JSON."

    assert "minimum_k" in data, "Key 'minimum_k' missing in JSON."
    assert "sv1_ratio" in data, "Key 'sv1_ratio' missing in JSON."
    assert "dominant_freq_index" in data, "Key 'dominant_freq_index' missing in JSON."

    assert data["minimum_k"] == 3, f"Expected minimum_k to be 3, got {data['minimum_k']}."
    assert abs(data["sv1_ratio"] - 2.158) < 1e-4, f"Expected sv1_ratio to be 2.158, got {data['sv1_ratio']}."
    assert data["dominant_freq_index"] == 25, f"Expected dominant_freq_index to be 25, got {data['dominant_freq_index']}."