# test_final_state.py
import os

def test_category_proto_fixed():
    category_proto = "/home/user/proto/category.proto"
    assert os.path.exists(category_proto), f"File {category_proto} is missing."

    with open(category_proto, 'r') as f:
        content = f.read()

    assert 'import "item.proto";' not in content, "Circular dependency 'import \"item.proto\";' is still in category.proto"
    assert 'Item top_item = 2;' not in content, "Field 'Item top_item = 2;' is still in category.proto"

def test_descriptor_pb_exists():
    descriptor_pb = "/home/user/descriptor.pb"
    assert os.path.exists(descriptor_pb), f"File {descriptor_pb} is missing."
    assert os.path.getsize(descriptor_pb) > 0, f"File {descriptor_pb} is empty."

def test_sorted_messages_txt():
    sorted_messages = "/home/user/sorted_messages.txt"
    assert os.path.exists(sorted_messages), f"File {sorted_messages} is missing."

    with open(sorted_messages, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert lines == ["Category", "Item"], f"Expected sorted messages to be ['Category', 'Item'], but got {lines}"

def test_nginx_grpc_conf_fixed():
    nginx_conf = "/home/user/nginx/grpc.conf"
    assert os.path.exists(nginx_conf), f"File {nginx_conf} is missing."

    with open(nginx_conf, 'r') as f:
        content = f.read()

    assert "grpc_pass grpc://localhost:50051;" in content, "Nginx config does not contain the correct 'grpc_pass grpc://localhost:50051;' directive."
    assert "proxy_pass" not in content, "Nginx config still contains 'proxy_pass' directive."