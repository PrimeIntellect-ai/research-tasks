# test_final_state.py

import os
import subprocess
import time
import socket
import threading

def test_cpp_file_exists():
    assert os.path.isfile("/home/user/finops_health_check.cpp"), "C++ source file /home/user/finops_health_check.cpp does not exist."

def test_script_exists_and_executable():
    script_path = "/home/user/deploy_finops.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cpp_compiles_and_runs():
    # Compile the C++ program manually to test its logic
    compile_cmd = ["g++", "/home/user/finops_health_check.cpp", "-o", "/tmp/finops_test_bin"]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Failed to compile C++ code:\n{res.stderr}"

    # Create a test conf
    conf_path = "/tmp/test_services.conf"
    with open(conf_path, "w") as f:
        f.write("127.0.0.1:19005\n127.0.0.1:19006\n")

    # Run with no listeners
    res = subprocess.run(["/tmp/finops_test_bin", conf_path], capture_output=True, text=True)
    assert res.returncode == 1, "C++ program should exit with code 1 when endpoints are down."
    assert "DOWN_REASON: 127.0.0.1:19005" in res.stdout or "DOWN_REASON: 127.0.0.1:19006" in res.stdout, "C++ program did not print DOWN_REASON correctly."

    # Start listeners
    def listener(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port))
        s.listen(1)
        try:
            s.settimeout(5)
            conn, addr = s.accept()
            conn.close()
        except Exception:
            pass
        finally:
            s.close()

    t1 = threading.Thread(target=listener, args=(19005,))
    t2 = threading.Thread(target=listener, args=(19006,))
    t1.start()
    t2.start()
    time.sleep(0.5)

    # Run with listeners
    res = subprocess.run(["/tmp/finops_test_bin", conf_path], capture_output=True, text=True)
    assert res.returncode == 0, "C++ program should exit with code 0 when all endpoints are up."
    assert "ALL_UP" in res.stdout, "C++ program did not print ALL_UP when successful."

    t1.join()
    t2.join()

def test_socat_forwarding():
    # The student's script should have started socat forwarding 8080 to 8081
    # Let's start a listener on 8081 and send data to 8080
    received_data = []

    def listener():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("127.0.0.1", 8081))
            s.listen(1)
            s.settimeout(3)
            conn, addr = s.accept()
            data = conn.recv(1024)
            received_data.append(data)
            conn.close()
        except Exception:
            pass
        finally:
            s.close()

    t = threading.Thread(target=listener)
    t.start()
    time.sleep(1)

    try:
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sender.connect(("127.0.0.1", 8080))
        sender.sendall(b"FINOPS_TEST")
        sender.close()
    except Exception as e:
        assert False, f"Failed to connect and send data to port 8080: {e}"

    t.join()
    assert len(received_data) > 0, "No data received on port 8081; socat forwarding might not be running or configured correctly."
    assert b"FINOPS_TEST" in received_data[0], "Data received on 8081 did not match what was sent to 8080."

def test_monitoring_loop_logging():
    log_path = "/home/user/cloud_health.log"
    # Wait to see if log is being written
    if os.path.exists(log_path):
        initial_size = os.path.getsize(log_path)
    else:
        initial_size = 0

    time.sleep(3)

    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    new_size = os.path.getsize(log_path)
    assert new_size > initial_size, "Log file is not being updated by the background monitoring loop."

    with open(log_path, "r") as f:
        content = f.read()

    assert "CLOUD_HEALTH: " in content, "Log file does not contain expected CLOUD_HEALTH output."