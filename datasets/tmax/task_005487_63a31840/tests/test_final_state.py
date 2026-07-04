# test_final_state.py
import os
import subprocess

def test_pipeline_status():
    status_file = "/home/user/pipeline_status.txt"
    assert os.path.isfile(status_file), f"Missing {status_file}. Did the pipeline run successfully?"
    with open(status_file, "r") as f:
        content = f.read().strip()
    assert content == "PIPELINE_SUCCESS", f"Expected PIPELINE_SUCCESS in {status_file}, got '{content}'"

def test_expr_c_visibility_fixed():
    expr_c = "/home/user/project/src/expr.c"
    assert os.path.isfile(expr_c), f"Missing {expr_c}"
    with open(expr_c, "r") as f:
        content = f.read()
    assert 'visibility("hidden")' not in content, "The evaluate_math function still has hidden visibility in src/expr.c"

def test_run_pipeline_fixed():
    pipeline = "/home/user/project/ci/run_pipeline.sh"
    assert os.path.isfile(pipeline), f"Missing {pipeline}"
    with open(pipeline, "r") as f:
        content = f.read()
    assert 'EXPECTED=$(echo "0")' not in content, "The expected calculation in run_pipeline.sh is still broken (hardcoded to 0)"
    assert '-shared' in content, "The gcc command for libexpr.so must use -shared"
    assert '-fPIC' in content, "The gcc command for libexpr.so must use -fPIC"

def test_artifacts_exist_and_work():
    lib_path = "/home/user/project/libexpr.so"
    cli_path = "/home/user/project/expr_cli"
    assert os.path.isfile(lib_path), f"Missing compiled library {lib_path}"
    assert os.path.isfile(cli_path), f"Missing compiled CLI {cli_path}"

    # Verify that the CLI actually works with the shared library
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/home/user/project"

    try:
        result = subprocess.run([cli_path, "5 + 7"], env=env, capture_output=True, text=True, timeout=2)
        assert result.returncode == 0, f"CLI execution failed with return code {result.returncode}. Stderr: {result.stderr}"
        assert result.stdout.strip() == "12", f"CLI output incorrect. Expected '12', got '{result.stdout.strip()}'"
    except Exception as e:
        assert False, f"Failed to execute {cli_path}: {e}"