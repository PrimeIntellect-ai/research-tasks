# test_final_state.py

import os
import json
import asyncio
import random
import subprocess
import time
import pytest
import websockets

def emulate_truth(code: str) -> str:
    """
    Ground truth emulator for the stack machine.
    """
    stack = []
    output = []
    tokens = code.split()
    for token in tokens:
        if token.startswith("P"):
            try:
                stack.append(int(token[1:]))
            except ValueError:
                pass
        elif token == "A":
            if len(stack) < 2:
                output.append("ERR")
                break
            a = stack.pop()
            b = stack.pop()
            # 64-bit integer simulation (Python handles arbitrarily large ints, but we wrap to 64-bit if needed.
            # For typical random programs, standard math is fine.)
            stack.append(b + a)
        elif token == "S":
            if len(stack) < 2:
                output.append("ERR")
                break
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif token == "M":
            if len(stack) < 2:
                output.append("ERR")
                break
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
        elif token == "O":
            if len(stack) < 1:
                output.append("ERR")
                break
            output.append(str(stack.pop()))

    res = "\n".join(output)
    if res:
        res += "\n"
    return res

def generate_random_program() -> str:
    tokens = []
    stack_size = 0
    for _ in range(random.randint(5, 50)):
        op = random.choice(["P", "A", "S", "M", "O", "ERR"])
        if op == "P" or stack_size < 2:
            tokens.append(f"P{random.randint(-100, 100)}")
            stack_size += 1
        elif op in ["A", "S", "M"]:
            tokens.append(op)
            stack_size -= 1
        elif op == "O":
            tokens.append("O")
            stack_size -= 1
        elif op == "ERR":
            # deliberately cause underflow sometimes
            tokens.append(random.choice(["A", "S", "M", "O"]))
            stack_size -= 2
    return " ".join(tokens)

@pytest.mark.asyncio
async def test_emulator_accuracy():
    server_path = "/home/user/server.py"
    assert os.path.exists(server_path), f"Server script {server_path} not found."

    # Start the server
    server_proc = subprocess.Popen(
        ["python3", server_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    await asyncio.sleep(2)

    correct_outputs = 0
    total_programs = 1000

    try:
        async with websockets.connect("ws://localhost:8765") as websocket:
            for i in range(total_programs):
                code = generate_random_program()
                expected_output = emulate_truth(code)

                client_id = f"test_client_{i}"
                payload = json.dumps({"client_id": client_id, "code": code})

                await websocket.send(payload)
                response_str = await websocket.recv()

                try:
                    response = json.loads(response_str)
                except json.JSONDecodeError:
                    response = {}

                actual_output = response.get("result", "")

                if actual_output == expected_output:
                    correct_outputs += 1

                # Sleep briefly to avoid rate limiting
                await asyncio.sleep(0.01)

    except Exception as e:
        server_proc.terminate()
        pytest.fail(f"Failed to communicate with the WebSocket server: {e}")
    finally:
        server_proc.terminate()
        server_proc.wait()

    accuracy = correct_outputs / total_programs
    assert accuracy >= 1.0, f"Accuracy {accuracy} is below the threshold of 1.0. Correct outputs: {correct_outputs}/{total_programs}"

def test_e2e_script_exists():
    e2e_path = "/home/user/e2e_test.py"
    assert os.path.exists(e2e_path), f"End-to-end test script {e2e_path} not found."