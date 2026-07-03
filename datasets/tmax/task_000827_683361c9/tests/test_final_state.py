# test_final_state.py
import os
import subprocess

def adler32(data: bytes) -> int:
    a = 1
    b = 0
    for byte in data:
        a = (a + byte) % 65521
        b = (b + a) % 65521
    return (b << 16) | a

def test_build_pipeline_exists_and_runs():
    """Verify that build_pipeline.sh exists and successfully runs."""
    pipeline_path = "/home/user/build_pipeline.sh"
    assert os.path.isfile(pipeline_path), f"Build pipeline script not found at {pipeline_path}"

    # Run the pipeline script
    result = subprocess.run(["bash", pipeline_path], capture_output=True, text=True)
    assert result.returncode == 0, f"build_pipeline.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_registry_csv_contents():
    """Verify the contents of the generated registry.csv file."""
    csv_path = "/home/user/registry.csv"
    assert os.path.isfile(csv_path), f"Output CSV not found at {csv_path}"

    expected_data = {
        "web_ui.tar": b"WEB_UI_MOCK_DATA",
        "api_server.bin": b"API_SERVER_MOCK_DATA",
        "legacy_db.so": b"LEGACY_DB_MOCK_DATA"
    }

    expected_lines = ["filename,checksum,security_status"]
    for filename, data in expected_data.items():
        checksum = adler32(data)
        expected_lines.append(f"{filename},{checksum},VERIFIED")

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"CSV contents do not match expected.\nExpected: {expected_lines}\nActual: {actual_lines}"

def test_rust_project_exists():
    """Verify that the Rust project was created at the correct location."""
    cargo_toml_path = "/home/user/audit-hash/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Rust project Cargo.toml not found at {cargo_toml_path}"

    main_rs_path = "/home/user/audit-hash/src/main.rs"
    assert os.path.isfile(main_rs_path), f"Rust project main.rs not found at {main_rs_path}"