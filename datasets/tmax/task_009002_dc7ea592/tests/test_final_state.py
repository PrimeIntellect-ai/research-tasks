# test_final_state.py
import os
import re

def test_setup_py_python3_compatible():
    setup_py = "/home/user/project/setup.py"
    assert os.path.isfile(setup_py), f"File {setup_py} is missing."
    with open(setup_py, "r") as f:
        content = f.read()
    assert 'print "' not in content, "setup.py still contains Python 2 print statements."
    assert 'print("' in content or 'print' not in content, "setup.py must be Python 3 compatible."

def test_semver_ext_c_python3_compatible():
    semver_c = "/home/user/project/semver_ext.c"
    assert os.path.isfile(semver_c), f"File {semver_c} is missing."
    with open(semver_c, "r") as f:
        content = f.read()
    assert "Py_InitModule" not in content, "semver_ext.c still uses Python 2 Py_InitModule."
    assert "PyModuleDef" in content, "semver_ext.c missing Python 3 PyModuleDef."
    assert "PyModule_Create" in content, "semver_ext.c missing Python 3 PyModule_Create."

def test_go_tester_exists():
    tester_go = "/home/user/project/tester.go"
    assert os.path.isfile(tester_go), f"File {tester_go} is missing."

def test_ci_sh_exists():
    ci_sh = "/home/user/project/ci.sh"
    assert os.path.isfile(ci_sh), f"File {ci_sh} is missing."

def test_success_log_contents():
    success_log = "/home/user/success.log"
    assert os.path.isfile(success_log), f"File {success_log} is missing. Did ci.sh run successfully?"

    with open(success_log, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "/api/v1/pkg/1.2.4" in lines, "Expected /api/v1/pkg/1.2.4 in success.log but it was missing."
    assert "/api/v1/pkg/2.0.0" in lines, "Expected /api/v1/pkg/2.0.0 in success.log but it was missing."

    assert "/api/v1/pkg/0.9.0" not in lines, "Found /api/v1/pkg/0.9.0 in success.log, but it should have failed the version check."
    assert "/api/v1/pkg/1.0.0-alpha" not in lines, "Found /api/v1/pkg/1.0.0-alpha in success.log, but it should have failed the version check."

    assert len(lines) == 2, f"Expected exactly 2 lines in success.log, found {len(lines)}."