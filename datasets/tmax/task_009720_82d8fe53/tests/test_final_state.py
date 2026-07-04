# test_final_state.py
import os
import re
import pytest

def parse_manifest(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    name_match = re.search(r'name:\s*([^\s]+)', content)
    name = name_match.group(1) if name_match else ''

    image_match = re.search(r'image:\s*([^\s]+)', content)
    image = image_match.group(1) if image_match else ''

    # Extract ports
    ports = []
    ports_section = re.search(r'ports:(.*?)(?:mounts:|EOF|\Z)', content, re.DOTALL)
    if ports_section:
        # Find all port and protocol pairs in order
        port_blocks = re.findall(r'-\s*port:\s*(\d+)\s*protocol:\s*([^\s]+)', ports_section.group(1))
        for p, proto in port_blocks:
            ports.append((p, proto))

    # Extract mounts
    mounts = []
    mounts_section = re.search(r'mounts:(.*?)(?:EOF|\Z)', content, re.DOTALL)
    if mounts_section:
        # Find all source, destination, fstype in order
        mount_blocks = re.findall(r'-\s*source:\s*([^\s]+)\s*destination:\s*([^\s]+)\s*fstype:\s*([^\s]+)', mounts_section.group(1))
        for s, d, fs in mount_blocks:
            mounts.append((s, d, fs))

    return {
        'name': name,
        'image': image,
        'ports': ports,
        'mounts': mounts
    }

def get_expected_outputs():
    manifests_dir = '/home/user/manifests'
    services = []
    if os.path.isdir(manifests_dir):
        for fname in os.listdir(manifests_dir):
            if fname.endswith('.yaml'):
                services.append(parse_manifest(os.path.join(manifests_dir, fname)))

    # Sort alphabetically by service name
    services.sort(key=lambda x: x['name'])

    fstab = []
    firewall = []
    containers = []

    for svc in services:
        for s, d, fs in svc['mounts']:
            fstab.append(f"{s} {d} {fs} defaults 0 0")
        for p, proto in svc['ports']:
            firewall.append(f"iptables -A INPUT -p {proto} --dport {p} -j ACCEPT")
        if svc['name'] and svc['image']:
            containers.append(f"podman run -d --name {svc['name']} {svc['image']}")

    return '\n'.join(fstab), '\n'.join(firewall), '\n'.join(containers)

def test_fstab_content():
    expected_fstab, _, _ = get_expected_outputs()
    file_path = '/home/user/output/fstab.conf'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path, 'r') as f:
        content = f.read().strip()
    assert content == expected_fstab.strip(), f"Content of {file_path} does not match the expected fstab format or order.\nExpected:\n{expected_fstab}\nGot:\n{content}"

def test_firewall_content():
    _, expected_firewall, _ = get_expected_outputs()
    file_path = '/home/user/output/firewall.sh'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path, 'r') as f:
        content = f.read().strip()
    assert content == expected_firewall.strip(), f"Content of {file_path} does not match the expected firewall rules or order.\nExpected:\n{expected_firewall}\nGot:\n{content}"

def test_containers_content():
    _, _, expected_containers = get_expected_outputs()
    file_path = '/home/user/output/containers.sh'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path, 'r') as f:
        content = f.read().strip()
    assert content == expected_containers.strip(), f"Content of {file_path} does not match the expected container commands or order.\nExpected:\n{expected_containers}\nGot:\n{content}"