# test_final_state.py

import os
import json
import subprocess
import requests
import pytest
import tempfile
import shutil

def expected_prediction(f1, f2, f3):
    ca = f1 * 2.0
    cb = f2 + 10.0
    cc = f3 if f3 > 0 else 0.0
    # True weights: 1.5, -0.8, 3.2. True bias: 5.0
    # target = 5.0 + 1.5 * ca - 0.8 * cb + 3.2 * cc
    return 5.0 + 1.5 * ca - 0.8 * cb + 3.2 * cc

def test_http_endpoint():
    url = "http://127.0.0.1:8080/predict"

    test_cases = [
        (1.0, 2.0, 3.0),
        (-1.0, -2.0, -3.0),
        (0.0, 0.0, 0.0),
        (2.5, -1.5, 4.2)
    ]

    for f1, f2, f3 in test_cases:
        payload = {"f1": f1, "f2": f2, "f3": f3}
        try:
            response = requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"HTTP request to {url} failed: {e}")

        assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "prediction" in data, f"Missing 'prediction' key in JSON response: {data}"

        pred = data["prediction"]
        expected = expected_prediction(f1, f2, f3)

        # Tolerance is 0.2 to account for L2 regularization and noise
        assert abs(pred - expected) < 0.2, f"Prediction {pred} is too far from expected {expected} for input {payload}"

def test_grpc_endpoint():
    # We will write a small Go client to test the gRPC endpoint
    # Requires protoc and Go to be available in the environment
    proto_path = "/home/user/predictor.proto"
    assert os.path.exists(proto_path), "predictor.proto is missing"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy proto file
        shutil.copy(proto_path, os.path.join(tmpdir, "predictor.proto"))

        # Initialize go module
        subprocess.run(["go", "mod", "init", "grpctest"], cwd=tmpdir, check=True, capture_output=True)

        # Generate protobuf code
        # We assume protoc and protoc-gen-go, protoc-gen-go-grpc are installed in the environment
        # If they are not, we will skip this test gracefully or fail if it's a strict requirement.
        gen_cmd = [
            "protoc",
            "--go_out=.",
            "--go-grpc_out=.",
            "predictor.proto"
        ]
        res = subprocess.run(gen_cmd, cwd=tmpdir, capture_output=True)
        if res.returncode != 0:
            # If protoc is not available or fails, we fallback to just checking if port is open
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(("127.0.0.1", 50051))
                s.close()
            except ConnectionRefusedError:
                pytest.fail("gRPC port 50051 is not open")
            return

        # Write Go client
        client_code = """
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "grpctest" // the generated package
)

func main() {
	conn, err := grpc.Dial("127.0.0.1:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewPredictorClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	r, err := c.Predict(ctx, &pb.PredictRequest{F1: 1.0, F2: 2.0, F3: 3.0})
	if err != nil {
		log.Fatalf("could not predict: %v", err)
	}
	fmt.Printf("%f", r.GetPrediction())
}
"""
        with open(os.path.join(tmpdir, "main.go"), "w") as f:
            f.write(client_code)

        subprocess.run(["go", "mod", "tidy"], cwd=tmpdir, check=True, capture_output=True)

        run_cmd = ["go", "run", "main.go"]
        res = subprocess.run(run_cmd, cwd=tmpdir, capture_output=True, text=True)

        if res.returncode != 0:
            pytest.fail(f"gRPC client execution failed: {res.stderr}")

        try:
            pred = float(res.stdout.strip())
        except ValueError:
            pytest.fail(f"Could not parse gRPC response as float: {res.stdout}")

        expected = expected_prediction(1.0, 2.0, 3.0)
        assert abs(pred - expected) < 0.2, f"gRPC Prediction {pred} is too far from expected {expected}"