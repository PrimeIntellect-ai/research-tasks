# test_final_state.py
import os
import socket

def test_cracked_pin_file():
    pin_file = "/home/user/cracked_pin.txt"
    assert os.path.exists(pin_file), f"File {pin_file} does not exist."
    with open(pin_file, "r") as f:
        content = f.read().strip()
    assert content == "4921", f"Expected PIN '4921' in {pin_file}, but found '{content}'."

def test_honeypot_script_exists_and_executable():
    script_file = "/home/user/honeypot.sh"
    assert os.path.exists(script_file), f"Script {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable."

def _test_tcp_interaction(pin_to_send, expected_response):
    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=3) as s:
            s.sendall(f"{pin_to_send}\n".encode("utf-8"))
            response = s.recv(1024).decode("utf-8").strip()
            assert response == expected_response, f"Expected '{expected_response}' for PIN {pin_to_send}, but got '{response}'."
    except ConnectionRefusedError:
        raise AssertionError("Connection refused on 127.0.0.1:9000. Is socat running?")
    except socket.timeout:
        raise AssertionError("Connection timed out waiting for response from 127.0.0.1:9000.")
    except Exception as e:
        raise AssertionError(f"An error occurred while connecting to 127.0.0.1:9000: {e}")

def test_socat_honeypot_correct_pin():
    _test_tcp_interaction("4921", "ACCESS_DENIED_HONEYPOT")

def test_socat_honeypot_incorrect_pin():
    _test_tcp_interaction("1111", "INVALID_PIN")