# test_final_state.py

import json
import os
import subprocess
import pytest

DEPLOY_DIR = "/home/user/deploy"

def test_result_txt_content():
    result_file = os.path.join(DEPLOY_DIR, "result.txt")
    assert os.path.isfile(result_file), f"{result_file} does not exist."
    with open(result_file, "r") as f:
        res = f.read().strip()
    assert res == "Result: 94", f"Expected 'Result: 94' in result.txt, but got '{res}'"

def test_deps_json_content():
    deps_file = os.path.join(DEPLOY_DIR, "deps.json")
    assert os.path.isfile(deps_file), f"{deps_file} does not exist."
    with open(deps_file, "r") as f:
        try:
            deps = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{deps_file} is not valid JSON.")

    assert isinstance(deps, dict), "deps.json should contain a dictionary."
    assert "math_engine" in deps, "math_engine missing from deps.json"
    assert "libcore.so" in deps["math_engine"], "math_engine should depend on libcore.so"
    assert "libcore.so" in deps, "libcore.so missing from deps.json"
    assert "libmath_ops.so" in deps["libcore.so"], "libcore.so should depend on libmath_ops.so"
    assert "libmath_ops.so" in deps, "libmath_ops.so missing from deps.json"

    # Tolerating either liblegacy.so or libmagic.so
    assert "liblegacy.so" in deps["libmath_ops.so"] or "libmagic.so" in deps["libmath_ops.so"], \
        "libmath_ops.so should depend on liblegacy.so or libmagic.so in deps.json"

def test_magic_assembly_exists():
    magic_s = os.path.join(DEPLOY_DIR, "magic.s")
    assert os.path.isfile(magic_s), f"{magic_s} does not exist."

def test_libmagic_so_exists():
    libmagic_so = os.path.join(DEPLOY_DIR, "libmagic.so")
    assert os.path.isfile(libmagic_so), f"{libmagic_so} does not exist."

def test_libmath_ops_linkage():
    libmath_ops_so = os.path.join(DEPLOY_DIR, "libmath_ops.so")
    assert os.path.isfile(libmath_ops_so), f"{libmath_ops_so} does not exist."

    try:
        output = subprocess.check_output(
            ["readelf", "-d", libmath_ops_so],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"readelf failed on {libmath_ops_so}: {e.output}")
    except FileNotFoundError:
        pytest.fail("readelf command not found. Ensure binutils is installed.")

    assert "libmagic.so" in output, f"libmath_ops.so does not have a NEEDED entry for libmagic.so. Output:\n{output}"
    assert "liblegacy.so" not in output, f"libmath_ops.so still has a NEEDED entry for liblegacy.so. Output:\n{output}"