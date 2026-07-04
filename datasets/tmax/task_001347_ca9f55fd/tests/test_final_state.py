# test_final_state.py
import os
import subprocess
import pytest

def test_eigen3_installed():
    # Check if Eigen3 headers are present
    assert os.path.exists("/usr/include/eigen3/Eigen/Dense"), "Eigen3 library does not appear to be installed at /usr/include/eigen3."

def test_likelihood_cpp_uses_svd():
    likelihood_path = "/home/user/bio_mcmc/likelihood.cpp"
    assert os.path.isfile(likelihood_path), f"File missing: {likelihood_path}"

    with open(likelihood_path, "r") as f:
        content = f.read()

    assert "JacobiSVD" in content, "likelihood.cpp does not use JacobiSVD as instructed."
    assert "LLT" not in content, "likelihood.cpp still contains LLT logic, which should have been replaced."

def test_build_and_run_mcmc():
    working_dir = "/home/user/bio_mcmc"

    # Run make clean and make to ensure we are testing the current code
    subprocess.run(["make", "clean"], cwd=working_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    build_res = subprocess.run(["make"], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert build_res.returncode == 0, f"Compilation failed:\n{build_res.stderr.decode()}"

    executable = os.path.join(working_dir, "mcmc_sampler")
    assert os.path.isfile(executable), "Executable mcmc_sampler was not created."

    run_res = subprocess.run([executable, "data.csv"], cwd=working_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert run_res.returncode == 0, f"Execution failed:\n{run_res.stderr.decode()}"

    output = run_res.stdout.decode().strip()

    # Check that output has 3 comma-separated values
    parts = output.split(",")
    assert len(parts) == 3, f"Expected 3 comma-separated values in output, got: {output}"
    try:
        [float(p) for p in parts]
    except ValueError:
        pytest.fail(f"Output values are not valid floats: {output}")

    # Check final_mean.txt
    final_txt_path = os.path.join(working_dir, "final_mean.txt")
    assert os.path.isfile(final_txt_path), f"File missing: {final_txt_path}"

    with open(final_txt_path, "r") as f:
        final_txt_content = f.read().strip()

    assert final_txt_content == output, f"Contents of final_mean.txt ('{final_txt_content}') do not match the program output ('{output}')."