# test_final_state.py

import os
import re
import pytest

def test_binary_exists_and_executable():
    """Test that the compiled Rust binary exists at the correct location and is executable."""
    binary_path = "/home/user/bin/main-app"
    assert os.path.exists(binary_path), f"Binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_service_dependencies_fixed():
    """Test that main-app.service has the correct dependencies configured."""
    service_path = "/home/user/.config/systemd/user/main-app.service"
    assert os.path.exists(service_path), f"Service file not found at {service_path}"

    with open(service_path, "r") as f:
        content = f.read()

    assert re.search(r"After\s*=\s*init-env\.service", content), "main-app.service is missing 'After=init-env.service'"
    assert re.search(r"Requires\s*=\s*init-env\.service", content), "main-app.service is missing 'Requires=init-env.service'"

def test_log_rotation_successful():
    """Test that log rotation was forced and created the rotated log file."""
    rotated_log_path = "/home/user/logs/app.log.1"
    assert os.path.exists(rotated_log_path), f"Rotated log file not found at {rotated_log_path}. Did you force logrotate?"

def test_service_status_reported():
    """Test that the service status was saved and indicates an active state."""
    status_file = "/home/user/service_status.txt"
    assert os.path.exists(status_file), f"Service status report not found at {status_file}"

    with open(status_file, "r") as f:
        content = f.read()

    assert "active" in content.lower(), f"Service status does not indicate it is active in {status_file}"

def test_log_dir_listing_reported():
    """Test that the log directory listing was saved and contains the expected files."""
    listing_file = "/home/user/log_dir_listing.txt"
    assert os.path.exists(listing_file), f"Log directory listing not found at {listing_file}"

    with open(listing_file, "r") as f:
        content = f.read()

    assert "app.log" in content, f"'app.log' missing from {listing_file}"
    assert "app.log.1" in content, f"'app.log.1' missing from {listing_file}"