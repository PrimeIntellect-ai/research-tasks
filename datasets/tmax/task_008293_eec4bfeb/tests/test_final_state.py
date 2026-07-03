# test_final_state.py
import os

def test_makefile_exists():
    makefile_path = "/home/user/qa_env/Makefile"
    assert os.path.isfile(makefile_path), "Makefile is missing at /home/user/qa_env/Makefile"

    with open(makefile_path, 'r') as f:
        content = f.read()

    assert "all:" in content, "Makefile must have a default 'all' target"

def test_test_runner_patched():
    runner_path = "/home/user/qa_env/test_env/test_runner.py"
    assert os.path.isfile(runner_path), f"File {runner_path} is missing"

    with open(runner_path, 'r') as f:
        content = f.read()

    assert "subprocess.run" in content, "test_runner.py does not appear to be patched. Missing subprocess.run logic."
    assert "routes.json" in content, "test_runner.py does not appear to be patched. Missing routes.json logic."

def test_results_log():
    log_path = "/home/user/qa_env/test_results.log"
    assert os.path.isfile(log_path), f"Log file is missing at {log_path}. Did the Makefile run successfully?"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected = """/users/:id | /users/123 => id:123
/api/v1/:resource/:action | /api/v1/posts/delete => action:delete
resource:posts
/static/:file | /api/v1/posts/delete => NOMATCH"""

    assert content == expected, f"Contents of {log_path} do not match the expected output. Got:\n{content}"