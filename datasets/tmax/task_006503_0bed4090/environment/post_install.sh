apt-get update && apt-get install -y python3 python3-pip jq bc wget curl
    pip3 install pytest websockets

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user

    cat << 'EOF' > /home/user/api_server.py
import asyncio
import websockets
import json

async def handler(websocket, path):
    data = [
        {"id": "01", "expr": "12 + 8"},
        {"id": "04", "expr": "50 - 15"},
        {"id": "02", "expr": "7 * 6"},
        {"id": "05", "expr": "100 * 3"},
        {"id": "03", "expr": "144 / 12"},
        {"id": "07", "expr": "20 + 35"},
        {"id": "06", "expr": "9 * 9"},
        {"id": "08", "expr": "64 / 8"},
        {"id": "10", "expr": "15 * 5"},
        {"id": "09", "expr": "200 - 45"},
        {"id": "11", "expr": "11 * 11"},
        {"id": "13", "expr": "500 / 10"},
        {"id": "12", "expr": "18 + 22"},
        {"id": "15", "expr": "75 - 25"},
        {"id": "14", "expr": "16 * 4"},
        {"id": "16", "expr": "81 / 9"},
        {"id": "18", "expr": "40 + 60"},
        {"id": "17", "expr": "13 * 3"},
        {"id": "20", "expr": "1000 / 8"},
        {"id": "19", "expr": "250 - 50"}
    ]
    for item in data:
        await websocket.send(json.dumps(item))
        await asyncio.sleep(0.01)

start_server = websockets.serve(handler, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
EOF

    cat << 'EOF' > /home/user/expected_results.txt
01 20
02 42
03 12
04 35
05 300
06 80
07 55
08 8
09 155
10 75
11 121
12 40
13 50
14 64
15 50
16 9
17 39
18 99
19 200
20 125
EOF

    chown -R user:user /home/user
    chmod -R 777 /home/user