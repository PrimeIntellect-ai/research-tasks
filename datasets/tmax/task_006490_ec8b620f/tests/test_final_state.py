# test_final_state.py

import os
import subprocess
import socket
import threading
import time
import pytest

def test_attacker_ip_identified():
    filepath = "/home/user/attacker_ip.txt"
    assert os.path.isfile(filepath), f"{filepath} is missing. Did you identify the attacker's IP?"

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "172.16.44.99", f"Incorrect attacker IP found in {filepath}."

def test_server_cpp_compiles():
    # Run make to verify server.cpp was fixed
    result = subprocess.run(
        ["make"], 
        cwd="/home/user/src", 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"make failed: {result.stderr.decode('utf-8')}"
    assert os.path.isfile("/home/user/src/server"), "/home/user/src/server executable was not built."

def test_reproduce_script_sends_correct_packets():
    script_path = "/home/user/reproduce.py"
    assert os.path.isfile(script_path), f"{script_path} is missing."

    received_payloads = []

    def udp_server():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", 9000))
        sock.settimeout(2.0)
        try:
            while True:
                data, _ = sock.recvfrom(1024)
                received_payloads.append(data.decode('utf-8', errors='ignore'))
        except socket.timeout:
            pass
        finally:
            sock.close()

    server_thread = threading.Thread(target=udp_server)
    server_thread.start()

    # Give the server a moment to start
    time.sleep(0.1)

    # Run the reproduce script
    result = subprocess.run(
        ["python3", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=3.0
    )

    server_thread.join()

    assert result.returncode == 0, f"reproduce.py failed to execute: {result.stderr.decode('utf-8')}"

    has_type_a = any(p.startswith("TYPE_A") for p in received_payloads)
    has_type_b = any(p.startswith("TYPE_B") for p in received_payloads)

    assert has_type_a and has_type_b, "reproduce.py did not send both TYPE_A and TYPE_B payloads to 127.0.0.1:9000."

def test_server_fixed_compiles_and_patched():
    fixed_src = "/home/user/src/server_fixed.cpp"
    assert os.path.isfile(fixed_src), f"{fixed_src} is missing."

    # Verify it compiles
    result = subprocess.run(
        ["g++", "-std=c++14", "server_fixed.cpp", "-o", "server_fixed", "-pthread"],
        cwd="/home/user/src",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"server_fixed.cpp failed to compile: {result.stderr.decode('utf-8')}"

    with open(fixed_src, "r") as f:
        content = f.read()

    # We expect the student to have fixed the deadlock.
    # A simple check is that they either used std::lock, std::scoped_lock, 
    # or changed the lock ordering so that it's consistent.
    # We will check that the naive inconsistent locking is no longer present exactly as it was.
    inconsistent_locking_a_then_b = "lock_guard<std::mutex> lock1(mutex_A);\n        std::this_thread::sleep_for(std::chrono::milliseconds(50));\n        std::lock_guard<std::mutex> lock2(mutex_B);"
    inconsistent_locking_b_then_a = "lock_guard<std::mutex> lock1(mutex_B);\n        std::this_thread::sleep_for(std::chrono::milliseconds(50));\n        std::lock_guard<std::mutex> lock2(mutex_A);"

    # Strip whitespace to make matching more robust against formatting changes
    stripped_content = "".join(content.split())
    naive_a_b = "lock_guard<std::mutex>lock1(mutex_A);std::this_thread::sleep_for(std::chrono::milliseconds(50));std::lock_guard<std::mutex>lock2(mutex_B);"
    naive_b_a = "lock_guard<std::mutex>lock1(mutex_B);std::this_thread::sleep_for(std::chrono::milliseconds(50));std::lock_guard<std::mutex>lock2(mutex_A);"

    assert not (naive_a_b in stripped_content and naive_b_a in stripped_content), \
        "server_fixed.cpp still appears to contain the inconsistent lock ordering deadlock."