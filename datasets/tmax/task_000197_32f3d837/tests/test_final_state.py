# test_final_state.py
import os
import sys
import importlib.util
import pytest

def test_build_success_log_exists():
    path = "/home/user/build_success.log"
    assert os.path.isfile(path), f"The success log {path} was not generated. Did you run the CI pipeline script?"

def test_build_success_log_content():
    path = "/home/user/build_success.log"
    assert os.path.isfile(path), f"The success log {path} was not generated."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "CI PASS", f"Expected 'CI PASS' in {path}, but got '{content}'."

def test_mock_loader_returns_sorted_routes():
    mock_loader_path = "/home/user/app/mock_loader.py"
    assert os.path.isfile(mock_loader_path), f"File {mock_loader_path} is missing."

    # Dynamically import the modified mock_loader
    spec = importlib.util.spec_from_file_location("mock_loader", mock_loader_path)
    mock_loader = importlib.util.module_from_spec(spec)
    sys.modules["mock_loader"] = mock_loader
    spec.loader.exec_module(mock_loader)

    routes = mock_loader.load_routing_mocks()
    assert len(routes) == 2, f"Expected exactly 2 routes to be loaded, got {len(routes)}."

    assert routes[0].get('path') == '/secure', "The first route loaded should be the secure route (/secure). Make sure the files are sorted."
    assert routes[1].get('path') == '/*', "The second route loaded should be the catch-all route (/*)."