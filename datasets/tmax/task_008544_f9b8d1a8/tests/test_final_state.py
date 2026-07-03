# test_final_state.py

import os
import re

WORKSPACE_DIR = "/home/user/workspace"
ROUTES_FILE = os.path.join(WORKSPACE_DIR, "routes.txt")
PROTO_FILE = os.path.join(WORKSPACE_DIR, "api.proto")

def test_routes_file_is_patched():
    """Ensure the patch was successfully applied to routes.txt."""
    assert os.path.isfile(ROUTES_FILE), f"File {ROUTES_FILE} does not exist"
    with open(ROUTES_FILE, "r") as f:
        content = f.read()

    assert "PUT /users/<int:user_id>/profile/<str:profile_type> UpdateProfile" in content, "Patch was not applied: new route missing."
    assert "DELETE /legacy/<str:resource_id> DeleteLegacy" not in content, "Patch was not applied: old route still present."

def test_api_proto_exists_and_content():
    """Ensure api.proto was generated and contains the correct definitions."""
    assert os.path.isfile(PROTO_FILE), f"File {PROTO_FILE} does not exist. C++ program may not have run or failed."

    with open(PROTO_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        content = " ".join(lines)
        raw_content = f.read()

    # Check basic protobuf structure
    assert 'syntax = "proto3";' in lines, "Missing or incorrect proto3 syntax declaration."
    assert 'package api;' in lines, "Missing or incorrect package declaration."

    # Check for the service definition and RPCs
    assert 'service ApiService {' in content or 'service ApiService{' in content, "Missing ApiService definition."

    # We expect specific RPC declarations based on the patched routes
    expected_rpcs = [
        "rpc HealthCheck(HealthCheckRequest) returns (HealthCheckResponse);",
        "rpc GetUser(GetUserRequest) returns (GetUserResponse);",
        "rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);",
        "rpc UpdateProfile(UpdateProfileRequest) returns (UpdateProfileResponse);"
    ]

    for rpc in expected_rpcs:
        # Remove spaces to do a robust check
        compact_rpc = rpc.replace(" ", "")
        compact_content = content.replace(" ", "")
        assert compact_rpc in compact_content, f"Missing or incorrectly formatted RPC: {rpc}"

    # Check for specific message fields
    # UpdateProfileRequest should have int32 user_id = 1; and string profile_type = 2;
    compact_content = content.replace(" ", "")
    assert "messageUpdateProfileRequest{int32user_id=1;stringprofile_type=2;}" in compact_content or \
           ("int32user_id=1;" in compact_content and "stringprofile_type=2;" in compact_content), \
           "Missing or incorrect fields in UpdateProfileRequest."

    # Check that response messages are empty
    assert "messageHealthCheckResponse{}" in compact_content, "HealthCheckResponse should be empty."
    assert "messageUpdateProfileResponse{}" in compact_content, "UpdateProfileResponse should be empty."