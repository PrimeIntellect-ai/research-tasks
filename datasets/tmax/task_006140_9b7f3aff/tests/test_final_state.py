# test_final_state.py
import os

def test_execution_order_file_exists_and_correct():
    path = "/home/user/execution_order.txt"
    assert os.path.isfile(path), f"File missing: {path}. The script likely failed to run or encountered a MemoryError."

    with open(path, "r") as f:
        actual_content = f.read().strip()

    expected_content = "Database,AuthService,Cache,UserService,API_Gateway,Frontend,Logging,Metrics"
    assert actual_content == expected_content, f"Content of {path} is incorrect. Expected '{expected_content}', got '{actual_content}'."

def test_service_resolver_retains_mock_data():
    path = "/home/user/service_resolver.py"
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "self._mock_env_data = bytearray(10 * 1024 * 1024)" in content, "The heavy state simulation (_mock_env_data) was removed or altered in service_resolver.py. You must fix the traversal logic itself."