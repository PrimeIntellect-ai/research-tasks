# test_final_state.py

import os
import re
import stat

HOME_DIR = "/home/user"
DATA_PIPELINE_DIR = os.path.join(HOME_DIR, "data_pipeline")
C_LIB_DIR = os.path.join(DATA_PIPELINE_DIR, "c_lib")
RUST_APP_DIR = os.path.join(DATA_PIPELINE_DIR, "rust_app")
RUST_SRC_DIR = os.path.join(RUST_APP_DIR, "src")

def test_makefile_and_libfilter():
    lib_path = os.path.join(C_LIB_DIR, "libfilter.a")
    assert os.path.isfile(lib_path), f"Static library {lib_path} was not created."

    makefile_path = os.path.join(C_LIB_DIR, "Makefile")
    with open(makefile_path, "r") as f:
        content = f.read()
        assert "ar " in content, "Makefile does not appear to use 'ar' to create the static library."

def test_build_rs_fixed():
    build_rs = os.path.join(RUST_APP_DIR, "build.rs")
    with open(build_rs, "r") as f:
        content = f.read()

    # Check that the link instructions are present and not commented out
    # We strip spaces to be resilient to formatting
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith("//")]
    joined_lines = "".join(lines)

    assert "cargo:rustc-link-search" in joined_lines, "build.rs is missing 'cargo:rustc-link-search' instruction."
    assert "cargo:rustc-link-lib" in joined_lines, "build.rs is missing 'cargo:rustc-link-lib' instruction."

def test_main_rs_lifetime_fixed():
    main_rs = os.path.join(RUST_SRC_DIR, "main.rs")
    with open(main_rs, "r") as f:
        content = f.read()

    # The intentional bug was inline CString::new(...).unwrap().as_ptr()
    bug_pattern = r"CString::new\([^)]+\)\.unwrap\(\)\.as_ptr\(\)"
    assert not re.search(bug_pattern, content), "main.rs still contains the inline CString::new(...).unwrap().as_ptr() lifetime bug."

def test_run_pipeline_script():
    script_path = os.path.join(HOME_DIR, "run_pipeline.sh")
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_results_txt():
    results_path = os.path.join(HOME_DIR, "results.txt")
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist. Did the script run successfully?"

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected_lines = ["MATCH: apple", "MATCH: banana"]
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Expected {expected_lines} in results.txt, but got {actual_lines}"

def test_bench_log_txt():
    bench_log_path = os.path.join(HOME_DIR, "bench_log.txt")
    assert os.path.isfile(bench_log_path), f"Benchmark log {bench_log_path} does not exist."

    with open(bench_log_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
        assert val >= 0.0, "Execution time cannot be negative."
    except ValueError:
        pytest.fail(f"bench_log.txt does not contain a valid float. Found: {content}")