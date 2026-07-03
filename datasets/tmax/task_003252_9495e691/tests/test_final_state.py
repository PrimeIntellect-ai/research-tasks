# test_final_state.py
import os
import stat

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_cleaned_data_exists_and_correct():
    cleaned_path = "/home/user/clean_data/cleaned_sensors.csv"
    assert os.path.isfile(cleaned_path), f"Cleaned data file {cleaned_path} does not exist."

    with open(cleaned_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "sensor_id,rack,temperature",
        "1,A,21.1",
        "2,A,21.5",
        "4,A,21.3",
        "6,A,21.2",
        "7,A,21.4",
        "8,B,21.6",
        "9,B,21.8",
        "11,B,21.5",
        "12,B,21.7",
        "13,B,21.9"
    ]

    assert lines == expected_lines, f"Cleaned data in {cleaned_path} does not match expected output."

def test_p_value_output():
    p_value_path = "/home/user/results/p_value.txt"
    assert os.path.isfile(p_value_path), f"Output file {p_value_path} does not exist."

    with open(p_value_path, "r") as f:
        content = f.read().strip()

    assert content == "0.0163", f"Expected p-value to be '0.0163', but got '{content}'."