# test_final_state.py
import os
import re

def test_rust_project_configuration():
    """Verify the Rust project is configured as a cdylib."""
    cargo_toml_path = "/home/user/rpn_calc/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"{cargo_toml_path} does not exist"

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    # Check for cdylib in crate-type
    assert re.search(r'crate-type\s*=\s*\[.*"cdylib".*\]', content), "Cargo.toml must configure crate-type as 'cdylib'"

def test_rust_lib_source():
    """Verify the Rust source code exposes the correct C ABI function."""
    lib_rs_path = "/home/user/rpn_calc/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"{lib_rs_path} does not exist"

    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "eval_rpn" in content, "lib.rs must contain the eval_rpn function"
    assert "#[no_mangle]" in content, "eval_rpn function must have #[no_mangle]"
    assert "extern \"C\"" in content, "eval_rpn function must use extern \"C\""

def test_c_frontend_source():
    """Verify the C frontend uses dlopen and dlsym."""
    frontend_c_path = "/home/user/frontend.c"
    assert os.path.isfile(frontend_c_path), f"{frontend_c_path} does not exist"

    with open(frontend_c_path, "r") as f:
        content = f.read()

    assert "dlopen" in content, "frontend.c must use dlopen"
    assert "dlsym" in content, "frontend.c must use dlsym"

def test_orchestration_script():
    """Verify the orchestration script exists and is executable."""
    script_path = "/home/user/run_e2e.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} must be executable"

def test_e2e_output():
    """Verify the output of the end-to-end execution is exactly correct."""
    output_path = "/home/user/e2e_output.txt"
    assert os.path.isfile(output_path), f"{output_path} does not exist. Did the script run successfully?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "5.00", f"Expected output '5.00', but got '{content}'"

def test_compiled_artifacts():
    """Verify the compiled artifacts are present in the user directory."""
    so_path = "/home/user/librpn_calc.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not copied to the user directory"

    bin_path = "/home/user/frontend"
    assert os.path.isfile(bin_path), f"Frontend binary {bin_path} was not compiled into the user directory"
    assert os.access(bin_path, os.X_OK), f"Frontend binary {bin_path} must be executable"