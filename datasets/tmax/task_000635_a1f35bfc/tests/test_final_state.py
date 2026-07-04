# test_final_state.py
import os

def test_rolling_sim_output():
    output_file = "/home/user/rolling_sim.csv"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    expected_content = (
        "Line,Jaccard,Rolling_Avg\n"
        "1,0.0000,0.0000\n"
        "2,1.0000,0.5000\n"
        "3,0.6250,0.5417\n"
        "4,0.0000,0.5417\n"
        "5,0.6000,0.4083"
    )

    with open(output_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {output_file} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{actual_content}"
    )

def test_c_source_exists():
    source_file = "/home/user/log_processor.c"
    assert os.path.exists(source_file), f"C source file {source_file} is missing."
    assert os.path.isfile(source_file), f"{source_file} is not a file."