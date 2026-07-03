# test_final_state.py
import os
import subprocess
import time
import signal
import pytest
import fcntl

def test_archiver_executable_exists():
    assert os.path.exists("/home/user/archiver"), "/home/user/archiver does not exist"
    assert os.access("/home/user/archiver", os.X_OK), "/home/user/archiver is not executable"

def test_archiver_behavior():
    # Clean up old files to ensure a fresh test
    for f in ["/home/user/repo.1.dat", "/home/user/repo.dat"]:
        if os.path.exists(f):
            os.remove(f)

    fifo_path = "/home/user/stream.fifo"
    if not os.path.exists(fifo_path):
        os.mkfifo(fifo_path)

    # Kill any existing archiver processes left running by the student
    subprocess.run(["pkill", "-9", "-f", "/home/user/archiver"], stderr=subprocess.DEVNULL)
    time.sleep(0.5)

    # Start the archiver
    proc = subprocess.Popen(["/home/user/archiver"])
    time.sleep(1)

    assert proc.poll() is None, "Archiver exited prematurely before receiving any data."

    try:
        # Open FIFO for writing. This will block if the archiver hasn't opened it for reading.
        # We use a lower-level open with a timeout via signal, or just rely on pytest timeout.
        fd = os.open(fifo_path, os.O_WRONLY)

        # Write test data part 1
        os.write(fd, b"\xAA" * 5)
        os.write(fd, b"\xBB" * 300)

        time.sleep(1)
        # Send SIGUSR1 to trigger rotation
        proc.send_signal(signal.SIGUSR1)
        time.sleep(1)

        # Write test data part 2
        os.write(fd, b"\xCC" * 10)
        time.sleep(1)

        # Send SIGTERM for graceful shutdown
        proc.send_signal(signal.SIGTERM)
        os.close(fd)

        # Wait for process to exit cleanly
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        pytest.fail("Archiver did not exit within 5 seconds after receiving SIGTERM.")
    except Exception as e:
        proc.kill()
        pytest.fail(f"Error interacting with archiver: {e}")

    # Verify repo.1.dat
    assert os.path.exists("/home/user/repo.1.dat"), "Rotated file /home/user/repo.1.dat was not created after SIGUSR1."
    with open("/home/user/repo.1.dat", "rb") as f:
        data1 = f.read()

    expected_data1 = b"\x05\xAA\xFF\xBB\x2D\xBB\x00\x00"
    assert data1 == expected_data1, f"repo.1.dat content incorrect. Expected {expected_data1.hex()}, got {data1.hex()}"

    # Verify repo.dat (final file before SIGTERM)
    assert os.path.exists("/home/user/repo.dat"), "Final file /home/user/repo.dat was not created or kept."
    with open("/home/user/repo.dat", "rb") as f:
        data2 = f.read()

    expected_data2 = b"\x0A\xCC\x00\x00"
    assert data2 == expected_data2, f"repo.dat content incorrect. Expected {expected_data2.hex()}, got {data2.hex()}"