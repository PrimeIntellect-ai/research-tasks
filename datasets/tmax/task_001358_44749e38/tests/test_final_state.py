# test_final_state.py

import os
import re
import time
import socket
import subprocess
import pytest

HOST = "127.0.0.1"
PORT = 8888

def send_command(cmd: str) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        s.connect((HOST, PORT))
        s.sendall(cmd.encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
    return response

def get_frame_count() -> int:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0", 
        "-count_packets", "-show_entries", "stream=nb_read_packets", 
        "-of", "csv=p=0", "/app/surveillance.mp4"
    ]
    output = subprocess.check_output(cmd, text=True).strip()
    return int(output)

def test_files_exist():
    assert os.path.isfile("/home/user/server.c"), "/home/user/server.c does not exist."
    assert os.path.isfile("/home/user/server"), "/home/user/server does not exist."
    assert os.path.isfile("/home/user/supervisor.sh"), "/home/user/supervisor.sh does not exist."

def test_elf_hardening():
    server_path = "/home/user/server"

    # Check PIE
    readelf_h = subprocess.check_output(["readelf", "-h", server_path], text=True)
    assert "DYN (Shared object file)" in readelf_h or "DYN (Position-Independent Executable" in readelf_h, "Executable is not built with PIE."

    # Check RELRO
    readelf_l = subprocess.check_output(["readelf", "-l", server_path], text=True)
    assert "GNU_RELRO" in readelf_l, "Executable is missing RELRO."

    # Check BIND_NOW (Full RELRO)
    readelf_d = subprocess.check_output(["readelf", "-d", server_path], text=True)
    assert "BIND_NOW" in readelf_d or "FLAGS_1" in readelf_d and "NOW" in readelf_d, "Executable is missing Full RELRO (-z now)."

    # Check stack protector
    readelf_s = subprocess.check_output(["readelf", "-s", server_path], text=True)
    assert "__stack_chk_fail" in readelf_s, "Executable is missing stack protector."

def test_supervisor_running():
    ps_output = subprocess.check_output(["ps", "aux"], text=True)
    assert "supervisor.sh" in ps_output, "supervisor.sh is not running in the background."

def test_server_count():
    expected_count = get_frame_count()
    response = send_command("COUNT\n")
    assert response == f"{expected_count}\n", f"Expected COUNT response '{expected_count}\\n', got '{response}'"

def test_server_time():
    response = send_command("TIME\n")
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} JST\n$"
    assert re.match(pattern, response), f"TIME response '{response}' does not match expected format."

def test_server_crash_and_restart():
    # Send CRASH
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((HOST, PORT))
            s.sendall(b"CRASH\n")
            s.recv(1024)
    except (socket.timeout, ConnectionResetError, EOFError):
        pass

    # Wait for supervisor to restart the server
    time.sleep(1.5)

    # Verify it's back up
    expected_count = get_frame_count()
    try:
        response = send_command("COUNT\n")
        assert response == f"{expected_count}\n", f"Expected COUNT response '{expected_count}\\n' after restart, got '{response}'"
    except ConnectionRefusedError:
        pytest.fail("Server did not restart after CRASH command.")