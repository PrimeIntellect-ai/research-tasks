# test_final_state.py

import os
import subprocess
import re
import pytest

def test_resolve_go_exists():
    assert os.path.exists("/home/user/resolve.go"), "/home/user/resolve.go does not exist."
    assert os.path.isfile("/home/user/resolve.go"), "/home/user/resolve.go is not a file."

def test_linux_binary_exists_and_format():
    binary_path = "/home/user/resolve_linux_amd64"
    assert os.path.exists(binary_path), f"{binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."

    # Check if it's an ELF file
    with open(binary_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{binary_path} is not an ELF executable."

def test_windows_binary_exists_and_format():
    binary_path = "/home/user/resolve_windows_amd64.exe"
    assert os.path.exists(binary_path), f"{binary_path} does not exist."
    assert os.path.isfile(binary_path), f"{binary_path} is not a file."

    # Check if it's a PE file
    with open(binary_path, "rb") as f:
        magic = f.read(2)
        assert magic == b"MZ", f"{binary_path} is not a PE executable."

def test_migration_sql():
    sql_path = "/home/user/migration.sql"
    assert os.path.exists(sql_path), f"{sql_path} does not exist."

    with open(sql_path, "r") as f:
        content = f.read().lower()

    # Check for ALTER TABLE deployments
    assert "alter table" in content and "deployments" in content, "Missing ALTER TABLE deployments statement."

    # Check for the two columns
    assert "resolved_version" in content, "Missing resolved_version column."
    assert "target_os" in content, "Missing target_os column."
    assert "varchar(50)" in content, "Missing VARCHAR(50) type."

def test_resolve_logic_worker_v1():
    binary_path = "/home/user/resolve_linux_amd64"
    url = "http://ci.local/resolve?pkg=worker&min_version=v1.0.0"

    result = subprocess.run([binary_path, url], capture_output=True, text=True)
    assert result.returncode == 0, f"Program exited with code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output == "v1.5.0", f"Expected 'v1.5.0', got '{output}'"

def test_resolve_logic_api_v1():
    binary_path = "/home/user/resolve_linux_amd64"
    url = "http://ci.local/resolve?pkg=api&min_version=v1.0.1"

    result = subprocess.run([binary_path, url], capture_output=True, text=True)
    assert result.returncode == 0, f"Program exited with code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output == "v1.2.0", f"Expected 'v1.2.0', got '{output}'"

def test_resolve_logic_none():
    binary_path = "/home/user/resolve_linux_amd64"
    url = "http://ci.local/resolve?pkg=worker&min_version=v3.0.0"

    result = subprocess.run([binary_path, url], capture_output=True, text=True)
    assert result.returncode == 0, f"Program exited with code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()
    assert output == "none", f"Expected 'none', got '{output}'"