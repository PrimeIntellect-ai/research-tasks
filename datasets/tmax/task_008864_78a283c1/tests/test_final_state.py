# test_final_state.py

import os
import subprocess
import hashlib
import pytest

SERVICES = [
    {"name": "service_auth", "depends_on": ["service_db", "service_cache"], "config_data": "auth_config_v2"},
    {"name": "service_db", "depends_on": ["service_network"], "config_data": "db_config_v2"},
    {"name": "service_cache", "depends_on": ["service_network"], "config_data": "cache_config_v2"},
    {"name": "service_api", "depends_on": ["service_auth", "service_logic"], "config_data": "api_config_v2"},
    {"name": "service_network", "depends_on": [], "config_data": "network_config_v2"},
    {"name": "service_logic", "depends_on": ["service_db"], "config_data": "logic_config_v2"}
]

def get_expected_hashes():
    return {
        svc["name"]: hashlib.sha256(svc["config_data"].encode('utf-8')).hexdigest()
        for svc in SERVICES
    }

def test_build_order_txt():
    """Verify build_order.txt exists and contains a valid topological sort."""
    build_order_path = "/home/user/build_order.txt"
    assert os.path.isfile(build_order_path), f"Missing {build_order_path}"

    with open(build_order_path, 'r') as f:
        content = f.read().strip()

    order = [s.strip() for s in content.split(',')]
    assert len(order) == len(SERVICES), "build_order.txt does not contain all services"

    # Check partial order constraints
    def index_of(svc):
        assert svc in order, f"{svc} missing from build_order.txt"
        return order.index(svc)

    assert index_of("service_network") < index_of("service_db"), "network must be before db"
    assert index_of("service_network") < index_of("service_cache"), "network must be before cache"
    assert index_of("service_db") < index_of("service_auth"), "db must be before auth"
    assert index_of("service_db") < index_of("service_logic"), "db must be before logic"
    assert index_of("service_cache") < index_of("service_auth"), "cache must be before auth"
    assert index_of("service_auth") < index_of("service_api"), "auth must be before api"
    assert index_of("service_logic") < index_of("service_api"), "logic must be before api"

def test_makefile_structure():
    """Verify the Makefile exists and has the correct targets."""
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"Missing {makefile_path}"

    with open(makefile_path, 'r') as f:
        lines = f.readlines()

    # Check first target is all
    first_target_line = None
    for line in lines:
        if line.strip() and not line.startswith('\t') and not line.startswith('#'):
            first_target_line = line
            break

    assert first_target_line is not None, "Makefile has no targets"
    assert first_target_line.startswith("all:"), "First target in Makefile must be 'all:'"

    for svc in SERVICES:
        assert svc["name"] in first_target_line, f"{svc['name']} missing from 'all' target"

def test_make_execution_and_build_files():
    """Run make and verify the generated .build files contain the correct hashes."""
    # Ensure Makefile is present
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"Missing {makefile_path}"

    # Run make
    result = subprocess.run(["make", "-C", "/home/user"], capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stderr}"

    expected_hashes = get_expected_hashes()

    for svc in SERVICES:
        build_file = f"/home/user/{svc['name']}.build"
        assert os.path.isfile(build_file), f"Missing build file {build_file} after running make"

        with open(build_file, 'r') as f:
            content = f.read().strip()

        expected_hash = expected_hashes[svc["name"]]
        assert content == expected_hash, f"Hash mismatch in {build_file}: expected {expected_hash}, got {content}"