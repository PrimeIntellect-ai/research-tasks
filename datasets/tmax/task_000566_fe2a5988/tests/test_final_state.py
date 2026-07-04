# test_final_state.py
import os
import sys
import pytest

def test_bad_commit_hash_correct():
    expected_hash_path = '/tmp/expected_bad_commit.txt'
    actual_hash_path = '/home/user/bad_commit_hash.txt'

    assert os.path.exists(expected_hash_path), f"Truth file {expected_hash_path} is missing."
    assert os.path.exists(actual_hash_path), f"Student file {actual_hash_path} is missing."

    with open(expected_hash_path, 'r') as f:
        expected_hash = f.read().strip()

    with open(actual_hash_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Commit hash mismatch. Expected {expected_hash}, got {actual_hash}."

def test_bin_parser_raises_correct_exception():
    repo_path = '/home/user/parser_repo'
    packet_path = '/home/user/crash_packet.bin'

    assert os.path.exists(repo_path), f"Repository path {repo_path} is missing."
    assert os.path.exists(packet_path), f"Crash packet {packet_path} is missing."

    sys.path.insert(0, repo_path)
    try:
        import bin_parser
    except ImportError as e:
        pytest.fail(f"Failed to import bin_parser: {e}")

    with open(packet_path, 'rb') as f:
        data = f.read()

    try:
        bin_parser.parse_packet(data)
        pytest.fail("parse_packet did not raise any exception, expected MalformedPacketError.")
    except bin_parser.MalformedPacketError as e:
        assert str(e) == "Payload too short", f"Incorrect exception message. Expected 'Payload too short', got '{str(e)}'."
    except Exception as e:
        pytest.fail(f"Raised incorrect exception type: {type(e).__name__} instead of MalformedPacketError.")
    finally:
        sys.path.remove(repo_path)