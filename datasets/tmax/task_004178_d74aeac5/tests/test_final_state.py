# test_final_state.py
import os
import stat

def test_eval_executable_exists():
    path = "/home/user/eval"
    assert os.path.isfile(path), f"The executable '{path}' was not found."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file '{path}' is not executable."

def test_proxy_conf_content():
    path = "/home/user/proxy.conf"
    assert os.path.isfile(path), f"The configuration file '{path}' was not found."

    expected_content = (
        "frontend main\n"
        "server backend1 10.0.0.1:45\n"
        "server backend2 10.0.0.2:20\n"
    )

    with open(path, 'r') as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"The contents of '{path}' do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_test_sh_not_bypassed():
    path = "/home/user/test.sh"
    assert os.path.isfile(path), f"The script '{path}' was not found."

    with open(path, 'r') as f:
        content = f.read()

    assert "backend1" in content, f"'{path}' appears to be bypassed or missing 'backend1' logic."
    assert "backend2" in content, f"'{path}' appears to be bypassed or missing 'backend2' logic."
    assert "&" in content, f"'{path}' must retain the concurrency (backgrounding '&') logic."