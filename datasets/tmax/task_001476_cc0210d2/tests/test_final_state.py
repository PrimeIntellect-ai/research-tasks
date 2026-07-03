# test_final_state.py

import os
import re
import ast

def test_setup_py_fixed():
    setup_path = "/home/user/data_ingester/setup.py"
    assert os.path.isfile(setup_path), f"{setup_path} is missing."

    with open(setup_path, "r") as f:
        content = f.read()

    # The missing comma should be fixed. We can check if it parses as valid Python.
    try:
        ast.parse(content)
    except SyntaxError as e:
        assert False, f"setup.py still contains a syntax error: {e}"

    # Also verify that both asyncio and logging are in the install_requires list
    # by evaluating the setup.py or just checking strings.
    assert "'asyncio'" in content or '"asyncio"' in content, "asyncio missing from setup.py"
    assert "'logging'" in content or '"logging"' in content, "logging missing from setup.py"
    assert "asyncio'logging" not in content.replace(" ", "").replace("\n", ""), "Comma is still missing between asyncio and logging."

def test_minimized_crash_bin():
    crash_path = "/home/user/minimized_crash.bin"
    assert os.path.isfile(crash_path), f"The file {crash_path} was not created."

    with open(crash_path, "rb") as f:
        content = f.read()

    assert b"\xBA\xAD\xF0\x0D" in content, "minimized_crash.bin does not contain the correct magic bytes."
    assert len(content) <= 16, "minimized_crash.bin is not properly minimized. It should contain only the minimal byte sequence."

def test_async_worker_fixed():
    worker_path = "/home/user/data_ingester/ingester/async_worker.py"
    assert os.path.isfile(worker_path), f"{worker_path} is missing."

    with open(worker_path, "r") as f:
        content = f.read()

    # Check if task_done is called in a finally block or multiple times (try + except)
    tree = ast.parse(content)

    class TaskDoneChecker(ast.NodeVisitor):
        def __init__(self):
            self.safe = False

        def visit_Try(self, node):
            # Check if task_done is in finally block
            finally_has_task_done = False
            for stmt in node.finalbody:
                if self._contains_task_done(stmt):
                    finally_has_task_done = True

            # Check if task_done is in except block
            except_has_task_done = False
            for handler in node.handlers:
                for stmt in handler.body:
                    if self._contains_task_done(stmt):
                        except_has_task_done = True

            # Check if task_done is in try block
            try_has_task_done = False
            for stmt in node.body:
                if self._contains_task_done(stmt):
                    try_has_task_done = True

            if finally_has_task_done or (try_has_task_done and except_has_task_done):
                self.safe = True

            self.generic_visit(node)

        def _contains_task_done(self, node):
            found = False
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Attribute) and child.func.attr == 'task_done':
                        found = True
            return found

    checker = TaskDoneChecker()
    checker.visit(tree)

    assert checker.safe, "async_worker.py does not properly call queue.task_done() for both success and exception paths."

def test_success_log():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"The file {log_path} was not created. Did the processor run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    match = re.match(r"Success:\s*(\d+),\s*Failed:\s*(\d+)", content)
    assert match, f"success.log content '{content}' does not match expected format 'Success: X, Failed: Y'."

    success_count = int(match.group(1))
    failed_count = int(match.group(2))

    assert success_count > 0, "Expected at least one successful record."
    assert failed_count > 0, "Expected at least one failed record (the malformed one)."