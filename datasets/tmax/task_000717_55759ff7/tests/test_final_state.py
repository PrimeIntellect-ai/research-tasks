# test_final_state.py
import os
import json
import socket

def test_processed_logs_json():
    json_path = "/home/user/processed_logs.json"
    assert os.path.exists(json_path), f"Processed logs JSON file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} contains invalid JSON."

    assert isinstance(data, list), "JSON root should be an array."

    # Check for XYZ-123
    xyz_record = next((item for item in data if item.get("record_id") == "XYZ-123"), None)
    assert xyz_record is not None, "Record XYZ-123 is missing from the processed JSON."
    assert xyz_record.get("lang") == "EN", "Record XYZ-123 should have lang 'EN' (earliest timestamp)."
    assert xyz_record.get("timestamp") == "2023-10-01T10:00:00Z", "Record XYZ-123 has incorrect timestamp."
    assert xyz_record.get("status") == "FAILED", "Record XYZ-123 has incorrect status."

    # Check for ABC-999
    abc_record = next((item for item in data if item.get("record_id") == "ABC-999"), None)
    assert abc_record is not None, "Record ABC-999 is missing from the processed JSON."
    assert abc_record.get("lang") == "ZH", "Record ABC-999 should have lang 'ZH'."
    assert abc_record.get("timestamp") == "2023-10-01T10:10:00Z", "Record ABC-999 has incorrect timestamp."
    assert abc_record.get("status") == "SUCCESS", "Record ABC-999 has incorrect status."

def test_grpc_port_open():
    host = "127.0.0.1"
    port = 50051
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        result = s.connect_ex((host, port))
        assert result == 0, f"gRPC server is not listening on {host}:{port}. Did you leave it running in the background?"