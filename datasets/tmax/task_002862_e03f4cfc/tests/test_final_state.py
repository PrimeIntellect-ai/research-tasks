# test_final_state.py

import os
import re

def test_init_api_script():
    filepath = '/home/user/init_api.py'
    assert os.path.exists(filepath), f"File {filepath} does not exist"

    with open(filepath, 'r') as f:
        content = f.read()

    assert '8080' in content, f"{filepath} does not contain port 8080"
    assert 'http.server' in content or 'HTTPServer' in content, f"{filepath} does not use http.server"
    assert '/home/user/api_data' in content, f"{filepath} does not reference the correct api_data directory"

def test_launch_node_script():
    filepath = '/home/user/launch_node.sh'
    assert os.path.exists(filepath), f"File {filepath} does not exist"

    with open(filepath, 'r') as f:
        content = f.read()

    assert 'qemu-system-aarch64' in content, f"{filepath} missing qemu-system-aarch64"
    assert '-M virt' in content or '-machine virt' in content, f"{filepath} missing virt machine type"
    assert '-m 512M' in content, f"{filepath} missing 512M memory"
    assert '-vnc :5' in content or '-display vnc=:5' in content, f"{filepath} missing VNC display 5"
    assert 'hostfwd=tcp::2222-:22' in content or 'hostfwd=tcp:127.0.0.1:2222-:22' in content or 'hostfwd=tcp:localhost:2222-:22' in content, f"{filepath} missing correct hostfwd for SSH"
    assert '/opt/iot_image.img' in content, f"{filepath} missing image path"
    assert 'virtio-net-pci' in content, f"{filepath} missing virtio-net-pci device"

def test_establish_tunnel_script():
    filepath = '/home/user/establish_tunnel.sh'
    assert os.path.exists(filepath), f"File {filepath} does not exist"

    with open(filepath, 'r') as f:
        content = f.read()

    assert 'ssh ' in content, f"{filepath} does not use ssh"
    assert '-R 9090:localhost:8080' in content or '-R 9090:127.0.0.1:8080' in content or '-R 9090::8080' in content, f"{filepath} missing correct reverse tunnel arguments (-R 9090:localhost:8080)"
    assert '-p 2222' in content, f"{filepath} missing port 2222"
    assert 'iotuser@localhost' in content or 'iotuser@127.0.0.1' in content, f"{filepath} missing target user/host (iotuser@localhost)"
    assert '-N' in content and '-f' in content, f"{filepath} missing background/no-command flags (-N -f)"
    assert 'StrictHostKeyChecking=no' in content, f"{filepath} missing StrictHostKeyChecking bypass"

def test_edge_client_script():
    filepath = '/home/user/edge_client.py'
    assert os.path.exists(filepath), f"File {filepath} does not exist"

    with open(filepath, 'r') as f:
        content = f.read()

    assert 'urllib.request' in content, f"{filepath} missing urllib.request"
    assert '127.0.0.1:9090/config.json' in content or 'localhost:9090/config.json' in content, f"{filepath} missing correct target URL"
    assert '/tmp/local_config.json' in content, f"{filepath} missing output file path"