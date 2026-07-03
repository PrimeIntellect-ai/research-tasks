# test_final_state.py
import os

def test_result_txt_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Expected {result_path} to exist."
    assert os.path.isfile(result_path), f"Expected {result_path} to be a file."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "0.45", f"Expected optimal beta in result.txt to be '0.45', but got '{content}'."

def test_plot_png_exists():
    plot_path = "/home/user/plot.png"
    assert os.path.exists(plot_path), f"Expected {plot_path} to exist."
    assert os.path.isfile(plot_path), f"Expected {plot_path} to be a file."
    assert os.path.getsize(plot_path) > 0, f"Expected {plot_path} to be a non-empty file."