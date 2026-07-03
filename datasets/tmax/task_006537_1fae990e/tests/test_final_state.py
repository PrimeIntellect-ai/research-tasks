# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/secure-parser"
RESULT_LOG = "/home/user/result.log"

def test_result_log_exists_and_correct():
    assert os.path.isfile(RESULT_LOG), f"Result log {RESULT_LOG} is missing."
    with open(RESULT_LOG, "r") as f:
        content = f.read().strip()

    expected_output = "Token: 57"
    assert content == expected_output, f"Expected output '{expected_output}', but got '{content}' in {RESULT_LOG}."

def test_evaluate_c_uses_malloc():
    filepath = os.path.join(PROJECT_DIR, "evaluate.c")
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    assert "malloc" in content, "evaluate.c does not appear to use malloc to allocate the return value dynamically."
    assert "return &result;" not in content, "evaluate.c still returns the address of a local variable."

def test_test_mock_c_uses_inline_assembly():
    filepath = os.path.join(PROJECT_DIR, "test_mock.c")
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    assert "asm" in content or "__asm__" in content, "test_mock.c does not appear to use inline assembly."
    assert "42" in content, "test_mock.c does not contain the secret key value 42."

def test_test_runner_compiled():
    exe_path = os.path.join(PROJECT_DIR, "test_runner")
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you run make?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_makefile_unmodified():
    filepath = os.path.join(PROJECT_DIR, "Makefile")
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    expected_makefile = """CFLAGS=-Wall -Werror -g

test_runner: evaluate.o test_mock.o
	gcc $(CFLAGS) -o test_runner $^

evaluate.o: evaluate.c ast.h lexer.h parser.h
	gcc $(CFLAGS) -c evaluate.c

test_mock.o: test_mock.c ast.h lexer.h parser.h
	gcc $(CFLAGS) -c test_mock.c

clean:
	rm -f *.o test_runner
"""
    assert content.strip() == expected_makefile.strip(), "Makefile was modified, which was forbidden by the instructions."