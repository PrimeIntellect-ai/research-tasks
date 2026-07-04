# test_final_state.py

import os
import subprocess
import shutil
import tempfile
import pytest

LOG_PARSER_DIR = "/home/user/log_parser"
ANOMALY_FILE = os.path.join(LOG_PARSER_DIR, "anomaly_line.txt")
PARSER_BIN = os.path.join(LOG_PARSER_DIR, "parser")
LOGS_FILE = os.path.join(LOG_PARSER_DIR, "logs.txt")
REGRESSION_TEST = os.path.join(LOG_PARSER_DIR, "regression_test.py")

def test_anomaly_line_correct():
    assert os.path.isfile(ANOMALY_FILE), f"{ANOMALY_FILE} is missing."
    with open(ANOMALY_FILE, "r") as f:
        content = f.read().strip()
    assert content == "4200", f"Expected anomaly line to be '4200', but got '{content}'."

def test_parser_fixed_and_runs():
    assert os.path.isfile(PARSER_BIN), f"{PARSER_BIN} is missing."
    assert os.access(PARSER_BIN, os.X_OK), f"{PARSER_BIN} is not executable."

    # Run the parser against the logs file
    result = subprocess.run([PARSER_BIN, LOGS_FILE], capture_output=True)
    assert result.returncode == 0, f"Parser crashed or failed on {LOGS_FILE}. Exit code: {result.returncode}"

def test_regression_test_passes():
    assert os.path.isfile(REGRESSION_TEST), f"{REGRESSION_TEST} is missing."

    # Run the regression test script
    result = subprocess.run(["python3", REGRESSION_TEST], cwd=LOG_PARSER_DIR, capture_output=True)
    assert result.returncode == 0, f"Regression test failed. Exit code: {result.returncode}\nStdout: {result.stdout.decode()}\nStderr: {result.stderr.decode()}"

def test_regression_test_fails_on_vulnerable_parser():
    # We will temporarily replace the parser binary with a vulnerable one to test the regression test
    vulnerable_c_code = """#include <stdio.h>
#include <string.h>

void process_log(const char *log_line) {
    char username[32];
    const char *user_ptr = strstr(log_line, "User:");
    if (user_ptr) {
        user_ptr += 5;
        const char *space_ptr = strchr(user_ptr, ' ');
        if (space_ptr) {
            int len = space_ptr - user_ptr;
            for(int i = 0; i < len; i++) {
                username[i] = user_ptr[i];
            }
            username[len] = '\\0';
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    char line[1024];
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    while (fgets(line, sizeof(line), f)) {
        process_log(line);
    }
    fclose(f);
    return 0;
}
"""
    backup_bin = PARSER_BIN + ".bak"
    if os.path.exists(PARSER_BIN):
        shutil.copy2(PARSER_BIN, backup_bin)

    try:
        # Compile vulnerable parser
        vuln_c = os.path.join(LOG_PARSER_DIR, "vuln_parser_test.c")
        with open(vuln_c, "w") as f:
            f.write(vulnerable_c_code)

        compile_res = subprocess.run(["gcc", "-O0", "-fno-stack-protector", "-o", PARSER_BIN, vuln_c], capture_output=True)
        assert compile_res.returncode == 0, "Failed to compile vulnerable parser for testing."

        # Run regression test
        result = subprocess.run(["python3", REGRESSION_TEST], cwd=LOG_PARSER_DIR, capture_output=True)
        assert result.returncode == 1, f"Regression test should have failed (exit code 1) with vulnerable parser, but it returned {result.returncode}."

    finally:
        # Restore original binary
        if os.path.exists(backup_bin):
            shutil.move(backup_bin, PARSER_BIN)
        if os.path.exists(os.path.join(LOG_PARSER_DIR, "vuln_parser_test.c")):
            os.remove(os.path.join(LOG_PARSER_DIR, "vuln_parser_test.c"))