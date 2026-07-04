# test_final_state.py

import os
import pytest

def test_rust_project_exists():
    """Verify that the Rust project was created."""
    project_dir = "/home/user/config_tracker"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")

    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} is missing."
    assert os.path.isfile(cargo_toml), f"Cargo.toml is missing in {project_dir}. Did you create a Rust project?"

def test_markdown_report_exists():
    """Verify that the output Markdown report exists."""
    report_path = "/home/user/hourly_report.md"
    assert os.path.isfile(report_path), f"Output report {report_path} is missing."

def test_markdown_report_content():
    """Verify that the output Markdown report has the exact expected content."""
    report_path = "/home/user/hourly_report.md"

    if not os.path.isfile(report_path):
        pytest.fail(f"Output report {report_path} is missing, cannot check content.")

    expected_content = (
        "# Configuration Change Report\n"
        "\n"
        "## Hour: 2023-10-01T10\n"
        "- srvA: max_conn (2)\n"
        "- srvB: motd (1)\n"
        "\n"
        "## Hour: 2023-10-01T11\n"
        "- srvA: timeout (2)\n"
        "\n"
        "## Hour: 2023-10-02T09\n"
        "- srvB: max_conn (1)\n"
        "- srvC: log_level (1)\n"
    )

    with open(report_path, "r", encoding="utf-8") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        "The content of the Markdown report does not match the expected output. "
        "Check formatting, sorting, and aggregation logic."
    )