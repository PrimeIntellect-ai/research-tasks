# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_build_script_exists_and_executable():
    script_path = "/home/user/build.sh"
    assert os.path.isfile(script_path), f"Build script {script_path} does not exist."
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Build script {script_path} is not executable."

def test_build_script_execution_and_output():
    # Execute the build script as the user
    build_result = subprocess.run(
        ["su", "-", "user", "-c", "/home/user/build.sh"],
        capture_output=True,
        text=True
    )
    assert build_result.returncode == 0, f"Build script failed to execute properly. Stderr: {build_result.stderr}"

    main_path = "/home/user/project/main"
    assert os.path.isfile(main_path), f"Executable {main_path} was not created."
    assert os.access(main_path, os.X_OK), f"File {main_path} is not executable."

    # Execute the compiled binary in a clean environment (no LD_LIBRARY_PATH)
    run_result = subprocess.run(
        ["su", "-", "user", "-c", "/home/user/project/main"],
        capture_output=True,
        text=True
    )
    assert run_result.returncode == 0, f"Running main failed. It may not be finding the shared libraries. Stderr: {run_result.stderr}"
    assert run_result.stdout.strip() == "Result: 52", f"Expected output 'Result: 52', but got: '{run_result.stdout.strip()}'"

def test_rpath_configured():
    main_path = "/home/user/project/main"
    if not os.path.isfile(main_path):
        pytest.fail(f"Executable {main_path} not found, cannot check rpath.")

    result = subprocess.run(["readelf", "-d", main_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run readelf to inspect the binary."

    has_correct_rpath = False
    for line in result.stdout.splitlines():
        if "(RPATH)" in line or "(RUNPATH)" in line:
            if "/home/user/project" in line or "$ORIGIN" in line:
                has_correct_rpath = True
                break

    assert has_correct_rpath, "RPATH or RUNPATH is not correctly set to /home/user/project or $ORIGIN in the main executable."