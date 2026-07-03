# test_final_state.py
import os
import sys
import subprocess
import pytest
import numpy as np
from scipy.special import expit

def test_proto_file_exists():
    assert os.path.exists('/home/user/service/calc.proto'), "calc.proto is missing"

def test_grpc_server_metrics():
    proto_path = '/home/user/service/calc.proto'
    assert os.path.exists(proto_path), "calc.proto is missing"

    # Compile proto
    compile_cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        "-I/home/user/service",
        "--python_out=/tmp",
        "--grpc_python_out=/tmp",
        proto_path
    ]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Failed to compile proto: {res.stderr}"

    sys.path.insert(0, '/tmp')

    try:
        import calc_pb2
        import calc_pb2_grpc
        import grpc
    except ImportError as e:
        pytest.fail(f"Failed to import generated proto modules: {e}")

    channel = grpc.insecure_channel('localhost:50051')
    stub_classes = [getattr(calc_pb2_grpc, c) for c in dir(calc_pb2_grpc) if 'Stub' in c]
    assert len(stub_classes) > 0, "No Stub class found in generated grpc module"
    stub = stub_classes[0](channel)

    # GetVersion
    req_classes = [c for c in dir(calc_pb2) if 'Req' in c and 'Vers' in c]
    v_req = None
    if not req_classes:
        empty_classes = [c for c in dir(calc_pb2) if 'Empty' in c]
        if empty_classes:
            v_req = getattr(calc_pb2, empty_classes[0])()
    else:
        v_req = getattr(calc_pb2, req_classes[0])()

    try:
        if v_req is not None:
            v_resp = stub.GetVersion(v_req)
        else:
            from google.protobuf.empty_pb2 import Empty
            v_resp = stub.GetVersion(Empty())
        assert "1.2.3" in str(v_resp), f"Semantic version 1.2.3 not found in response: {v_resp}"
    except Exception as e:
        pytest.fail(f"GetVersion RPC failed: {e}")

    # ComputeSigmoid
    inputs = np.linspace(-10, 10, 10000).astype(float).tolist()
    sig_req_classes = [c for c in dir(calc_pb2) if 'Sigmoid' in c or 'Req' in c and 'Vers' not in c]

    req_class = None
    for c in sig_req_classes:
        try:
            desc = getattr(calc_pb2, c).DESCRIPTOR
            if any(f.label == 3 for f in desc.fields): # repeated field
                req_class = getattr(calc_pb2, c)
                break
        except AttributeError:
            continue

    assert req_class is not None, "Could not find a Request message with a repeated field for ComputeSigmoid"

    repeated_field_in = [f.name for f in req_class.DESCRIPTOR.fields if f.label == 3][0]
    req_kwargs = {repeated_field_in: inputs}
    req = req_class(**req_kwargs)

    try:
        resp = stub.ComputeSigmoid(req)
    except Exception as e:
        pytest.fail(f"ComputeSigmoid RPC failed: {e}")

    repeated_field_out_list = [f.name for f in resp.DESCRIPTOR.fields if f.label == 3]
    assert len(repeated_field_out_list) > 0, "Response message has no repeated field"
    repeated_field_out = repeated_field_out_list[0]

    outputs = np.array(getattr(resp, repeated_field_out))
    expected = expit(inputs)

    assert len(outputs) == len(expected), f"Output length mismatch: {len(outputs)} vs {len(expected)}"
    mse = np.mean((outputs - expected)**2)

    assert mse <= 1e-4, f"MSE {mse} is greater than threshold 1e-4"