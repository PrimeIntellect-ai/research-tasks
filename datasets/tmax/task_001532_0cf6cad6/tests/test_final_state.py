# test_final_state.py
import os
import stat

def test_aggregate_cpp_exists():
    path = "/home/user/aggregate.cpp"
    assert os.path.isfile(path), f"File {path} is missing. The C++ program source code must be created."

def test_pipeline_sh_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"File {path} is missing. The ETL pipeline script must be created."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable. Make sure to run chmod +x on it."

def test_summary_csv_exists_and_correct():
    path = "/home/user/summary.csv"
    assert os.path.isfile(path), f"File {path} is missing. The pipeline must generate this output file."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "S1,10000000.250000,0.016667\n"
        "S2,50000000.525000,0.002500"
    )

    assert content == expected_content, (
        f"Contents of {path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nGot:\n{content}\n"
        "Check your data cleaning logic and ensure your C++ variance calculation is numerically stable."
    )