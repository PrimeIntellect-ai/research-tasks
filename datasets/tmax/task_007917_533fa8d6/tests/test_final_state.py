# test_final_state.py
import os
import stat

def test_audit_report():
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"Audit report {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "PIN: 4829", f"Audit report content is incorrect. Expected 'PIN: 4829', got '{content}'"

def test_flag_txt_content_and_permissions():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"Flag file {flag_path} does not exist."

    with open(flag_path, "r") as f:
        content = f.read()

    assert content == "CONFIDENTIAL_DATA_9921\n", "Flag file content is incorrect."

    st = os.stat(flag_path)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Flag file permissions are incorrect. Expected 0400, got {oct(permissions)}"

def test_rust_project_exists():
    project_dir = "/home/user/cracker"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."

    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    main_rs = os.path.join(project_dir, "src", "main.rs")

    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}."
    assert os.path.isfile(main_rs), f"src/main.rs not found in {project_dir}."