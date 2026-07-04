You are a QA engineer tasked with building a reliable data processing component and its CI testing pipeline. The data engineering team needs a numerically stable implementation of sample variance using Welford's online algorithm, along with rigorous property-based tests.

Please complete the following steps:

1. Create a directory at `/home/user/qa_project`.
2. Inside this directory, create a Python file named `welford.py`. Implement a single function:
   `def calculate_sample_variance(data: list[float]) -> float:`
   This function MUST compute the sample variance of the input list using Welford's online algorithm to ensure numerical stability.
   - If the input list has fewer than 2 elements, it must raise a `ValueError`.
3. Create a test file named `test_welford.py` in the same directory. Use `pytest` and the `hypothesis` library to write property-based tests for your function. You must test at least the following two properties:
   - **Non-negativity:** The computed variance must always be >= -1e-9 (accounting for tiny floating point inaccuracies).
   - **Shift Invariance:** Adding a random constant float `C` to every element in the list should not change the variance (use `math.isclose` with `rel_tol=1e-5`, `abs_tol=1e-8` for comparison).
   - *Note: Limit your hypothesis strategies to generate lists of floats between -1000.0 and 1000.0, with minimum length 2, avoiding NaNs and Infs.*
4. Create a bash script at `/home/user/qa_project/run_pipeline.sh`. This script will act as a local CI/CD pipeline step. It must:
   - Create a Python virtual environment at `/home/user/qa_project/venv`.
   - Activate the virtual environment.
   - Install `pytest` and `hypothesis`.
   - Run `pytest test_welford.py`.
   - If the tests pass successfully (exit code 0), write the exact string `PIPELINE_SUCCESS` to `/home/user/pipeline_result.log`. If they fail, write `PIPELINE_FAILURE`.
5. Make sure the script is executable and execute `/home/user/qa_project/run_pipeline.sh` so that the log file is generated.