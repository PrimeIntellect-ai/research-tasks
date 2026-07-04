# test_final_state.py
import os
import ast
import re

PROJECT_DIR = '/home/user/project'
SERVER_FILE = os.path.join(PROJECT_DIR, 'server.py')

def test_protobuf_compiled():
    pb2_file = os.path.join(PROJECT_DIR, 'calc_pb2.py')
    pb2_grpc_file = os.path.join(PROJECT_DIR, 'calc_pb2_grpc.py')

    assert os.path.isfile(pb2_file), f"{pb2_file} is missing. Protobuf was not compiled."
    assert os.path.isfile(pb2_grpc_file), f"{pb2_grpc_file} is missing. Protobuf was not compiled."

def test_server_file_exists():
    assert os.path.isfile(SERVER_FILE), f"{SERVER_FILE} is missing."

def test_rate_limiter_logic():
    with open(SERVER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    tree = ast.parse(content)

    # Find RateLimiter class
    rate_limiter_class = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == 'RateLimiter':
            rate_limiter_class = node
            break

    assert rate_limiter_class is not None, "RateLimiter class not found in server.py"

    # Check if it uses a dictionary or similar to track per-client state
    init_func = None
    allow_func = None
    for node in rate_limiter_class.body:
        if isinstance(node, ast.FunctionDef):
            if node.name == '__init__':
                init_func = node
            elif node.name == 'allow':
                allow_func = node

    assert init_func is not None, "RateLimiter.__init__ missing"
    assert allow_func is not None, "RateLimiter.allow missing"

    # We expect some dict assignment in __init__ or allow
    has_dict = "dict" in content or "{}" in content or "defaultdict" in content
    assert has_dict, "RateLimiter does not seem to use a dictionary to track per-client state."

    # Check if client_id is used in allow
    args = [arg.arg for arg in allow_func.args.args]
    assert 'client_id' in args, "RateLimiter.allow must take client_id as an argument."

def test_input_validation_and_safety():
    with open(SERVER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for length limit of 50
    assert "50" in content, "Could not find length limit of 50 in server.py"

    # Check for character restrictions (regex or explicit character checks)
    has_char_check = re.search(r'[\+\-\*/\(\)\.\s0-9]', content) is not None
    assert has_char_check, "Could not find character whitelist validation in server.py"

    # Check for try/except blocks around decode and eval
    tree = ast.parse(content)
    eval_in_try = False
    decode_in_try = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            try_body_code = ast.unparse(node.body)
            if 'eval(' in try_body_code:
                eval_in_try = True
            if 'b64decode' in try_body_code or 'decode' in try_body_code:
                decode_in_try = True

    assert decode_in_try, "Base64 decoding must be wrapped in a try/except block to catch errors."
    assert eval_in_try, "The eval() function must be wrapped in a try/except block to catch evaluation errors."

def test_grpc_status_codes_used():
    with open(SERVER_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "grpc.StatusCode.RESOURCE_EXHAUSTED" in content, "Must use grpc.StatusCode.RESOURCE_EXHAUSTED for rate limiting."
    assert "grpc.StatusCode.INVALID_ARGUMENT" in content, "Must use grpc.StatusCode.INVALID_ARGUMENT for validation/evaluation errors."