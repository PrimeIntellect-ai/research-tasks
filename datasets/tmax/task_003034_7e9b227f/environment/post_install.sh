apt-get update && apt-get install -y python3 python3-pip redis-server
    pip3 install --no-cache-dir pytest fastapi uvicorn redis grpcio grpcio-tools protobuf python-dotenv httpx

    mkdir -p /home/user/services/gateway
    mkdir -p /home/user/services/compute

    # Create gateway .env
    cat << 'EOF' > /home/user/services/gateway/.env
COMPUTE_GRPC_URL=127.0.0.1:9999
EOF

    # Create proto file and generate python code
    cat << 'EOF' > /home/user/services/compute/compute.proto
syntax = "proto3";
package compute;

service ComputeNode {
    rpc GetRecommendations (RecommendationRequest) returns (RecommendationResponse) {}
}

message RecommendationRequest {
    int32 user_id = 1;
}

message RecommendationResponse {
    repeated string recommendations = 1;
}
EOF

    python3 -m grpc_tools.protoc -I/home/user/services/compute --python_out=/home/user/services/compute --grpc_python_out=/home/user/services/compute /home/user/services/compute/compute.proto

    # Copy generated files to gateway as well
    cp /home/user/services/compute/compute_pb2.py /home/user/services/gateway/
    cp /home/user/services/compute/compute_pb2_grpc.py /home/user/services/gateway/

    # Create compute processor
    cat << 'EOF' > /home/user/services/compute/processor.py
import redis

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

def resolve_graph(user_id, depth=0):
    # Bug: missing base case for user_ids that are multiples of 7
    if user_id % 7 == 0:
        # Endless loop
        return resolve_graph(user_id, depth + 1)

    if depth > 5:
        return []

    return [f"item_{user_id}_{depth}"]
EOF

    # Create compute server
    cat << 'EOF' > /home/user/services/compute/server.py
import grpc
from concurrent import futures
import time
import compute_pb2
import compute_pb2_grpc
from processor import resolve_graph

class ComputeNodeServicer(compute_pb2_grpc.ComputeNodeServicer):
    def GetRecommendations(self, request, context):
        recs = resolve_graph(request.user_id)
        return compute_pb2.RecommendationResponse(recommendations=recs)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    compute_pb2_grpc.add_ComputeNodeServicer_to_server(ComputeNodeServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
EOF

    # Create gateway main
    cat << 'EOF' > /home/user/services/gateway/main.py
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import grpc
import os
from dotenv import load_dotenv
import compute_pb2
import compute_pb2_grpc

load_dotenv()

app = FastAPI()

COMPUTE_GRPC_URL = os.getenv("COMPUTE_GRPC_URL", "127.0.0.1:9999")

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int, x_auth_token: str = Header(None)):
    if x_auth_token != "emergency-bypass":
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        channel = grpc.insecure_channel(COMPUTE_GRPC_URL)
        stub = compute_pb2_grpc.ComputeNodeStub(channel)
        response = stub.GetRecommendations(compute_pb2.RecommendationRequest(user_id=user_id), timeout=2)
        return {"user_id": user_id, "recommendations": list(response.recommendations)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user