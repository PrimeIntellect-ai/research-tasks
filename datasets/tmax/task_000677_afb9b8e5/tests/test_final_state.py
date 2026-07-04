# test_final_state.py
import socket
import zlib
import pytest

HOST = '127.0.0.1'
PORT = 8888
AUTH_KEY = 'BKP-8821-X9'

def test_bad_auth_key():
    """Verify that an invalid auth key results in immediate connection closure with no data."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((HOST, PORT))
        s.sendall(b'FETCH_BACKUP INVALID-KEY\n')
        data = s.recv(4096)
        assert not data, "Server should not return data for an invalid auth key, but it did."
    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}. Is it running?")
    finally:
        s.close()

def test_backup_server_success():
    """Verify that a valid auth key returns the correct zlib-compressed, redacted log stream."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((HOST, PORT))
        s.sendall(f'FETCH_BACKUP {AUTH_KEY}\n'.encode('utf-8'))

        data = b''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk

        assert data, "Server returned no data for a valid auth key."

        try:
            decompressed = zlib.decompress(data).decode('utf-8')
        except zlib.error:
            pytest.fail("Returned data is not valid zlib compressed data.")
        except UnicodeDecodeError:
            pytest.fail("Decompressed data is not valid UTF-8 text.")

        # Check exclusions
        assert "rotating..." not in decompressed, "Included file <= 50 bytes (e.g., log2.log)."
        assert "12345678" not in decompressed, "Included non .log file (e.g., config.txt)."

        # Check redactions
        assert "SECRET_TOKEN=x9A4b2C1" not in decompressed, "Failed to redact log1."
        assert "SECRET_TOKEN=99zzAA11" not in decompressed, "Failed to redact log3 (first token)."
        assert "SECRET_TOKEN=00000000" not in decompressed, "Failed to redact log3 (second token)."

        # Check expected redacted text and content exists
        assert "SECRET_TOKEN=REDACTED" in decompressed, "Redacted text missing from the output stream."
        assert "USER=admin" in decompressed, "Missing valid log content from log1."
        assert "USER=guest" in decompressed, "Missing valid log content from log3."

    except ConnectionRefusedError:
        pytest.fail(f"Could not connect to server at {HOST}:{PORT}. Is it running?")
    finally:
        s.close()