# test_final_state.py

import os
import sys
import pytest

def test_build_artifacts():
    cpp_bin = "/app/bin/engine_cpp"
    go_bin = "/app/bin/engine_go"

    assert os.path.isfile(cpp_bin), f"Build artifact missing: {cpp_bin}"
    assert os.access(cpp_bin, os.X_OK), f"Build artifact is not executable: {cpp_bin}"

    assert os.path.isfile(go_bin), f"Build artifact missing: {go_bin}"
    assert os.access(go_bin, os.X_OK), f"Build artifact is not executable: {go_bin}"

def test_nginx_config():
    nginx_conf = "/app/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf), f"Nginx configuration missing: {nginx_conf}"
    with open(nginx_conf, 'r') as f:
        content = f.read()
        assert "8080" in content, "Nginx config does not seem to listen on port 8080"

def test_sanitizer_clean_corpus():
    sys.path.append('/app/src/python')
    try:
        from sanitizer import is_safe_math
    except ImportError:
        pytest.fail("Could not import is_safe_math from /app/src/python/sanitizer.py")

    clean_path = "/app/corpora/clean.txt"
    assert os.path.isfile(clean_path), f"Clean corpus missing at {clean_path}"

    with open(clean_path, 'r') as f:
        clean_exprs = [line.strip() for line in f if line.strip()]

    failed = []
    for expr in clean_exprs:
        try:
            if not is_safe_math(expr):
                failed.append(expr)
        except Exception:
            # If it raises an exception on clean data, it's considered rejected
            failed.append(expr)

    if failed:
        pytest.fail(f"{len(failed)} of {len(clean_exprs)} clean modified/rejected. Offending: {failed[:5]}")

def test_sanitizer_evil_corpus():
    sys.path.append('/app/src/python')
    try:
        from sanitizer import is_safe_math
    except ImportError:
        pytest.fail("Could not import is_safe_math from /app/src/python/sanitizer.py")

    evil_path = "/app/corpora/evil.txt"
    assert os.path.isfile(evil_path), f"Evil corpus missing at {evil_path}"

    with open(evil_path, 'r') as f:
        evil_exprs = [line.strip() for line in f if line.strip()]

    failed = []
    for expr in evil_exprs:
        try:
            if is_safe_math(expr):
                failed.append(expr)
        except Exception:
            # Raising an exception on evil data is an acceptable form of rejection
            pass

    if failed:
        pytest.fail(f"{len(failed)} of {len(evil_exprs)} evil bypassed. Offending: {failed[:5]}")