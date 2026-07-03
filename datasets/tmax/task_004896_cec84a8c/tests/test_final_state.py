# test_final_state.py

import os
import json

def test_build_py_patched():
    path = "/home/user/build_env/build.py"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "--link-order" in content, "build.py was not patched correctly (missing --link-order argument)."
    assert "build_artifact.bin" in content, "build.py was not patched correctly (missing artifact generation)."

def test_link_order_txt():
    path = "/home/user/build_env/link_order.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you save the computed build sequence?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = [
        "libauth_stub",
        "libfs",
        "libdb",
        "libauth",
        "libnet",
        "libcrypto",
        "libhttp",
        "main"
    ]

    assert lines == expected_order, f"The build sequence in link_order.txt is incorrect.\nExpected: {expected_order}\nGot: {lines}"

def test_build_artifact_bin():
    path = "/home/user/build_env/build_artifact.bin"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the patched build script?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = "SUCCESS: libauth_stub,libfs,libdb,libauth,libnet,libcrypto,libhttp,main"
    assert content == expected_content, f"The content of build_artifact.bin is incorrect.\nExpected: {expected_content}\nGot: {content}"