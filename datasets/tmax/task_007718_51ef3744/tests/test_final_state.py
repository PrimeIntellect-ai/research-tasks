# test_final_state.py
import os
import subprocess

def test_kde_c_exists():
    assert os.path.isfile('/home/user/kde.c'), "/home/user/kde.c does not exist."

def test_plot_kde_py_exists():
    assert os.path.isfile('/home/user/plot_kde.py'), "/home/user/plot_kde.py does not exist."

def test_test_kde_sh_runs_successfully():
    script_path = '/home/user/test_kde.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Run the bash script
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_density_output_content():
    output_path = '/home/user/density_output.txt'
    assert os.path.isfile(output_path), f"{output_path} was not created."

    with open(output_path, 'r') as f:
        content = f.read()

    # Check for the specific line
    expected_line = "0.0,0.33795"
    assert expected_line in content, f"Expected line '{expected_line}' not found in {output_path}."

def test_density_plot_png_exists():
    plot_path = '/home/user/density_plot.png'

    # If it doesn't exist, try running the python script
    if not os.path.isfile(plot_path):
        py_script = '/home/user/plot_kde.py'
        if os.path.isfile(py_script):
            subprocess.run(['python3', py_script], capture_output=True)

    assert os.path.isfile(plot_path), f"{plot_path} does not exist."
    assert os.path.getsize(plot_path) > 0, f"{plot_path} is empty (size 0)."