apt-get update && apt-get install -y python3 python3-pip binutils
    pip3 install pytest pyinstaller

    # Create the python script for the dataset packager
    cat << 'EOF' > /tmp/packager.py
import sys
import json
import struct
import os

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    with open(input_file, 'r') as f:
        data = json.load(f)

    id_str = data['id']
    category = data['category']
    data_list = data['data']

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, category), exist_ok=True)

    payload = b'PACK'
    id_bytes = id_str.encode('ascii')
    payload += struct.pack('<I', len(id_bytes))
    payload += id_bytes
    payload += struct.pack('<I', len(data_list))
    for val in data_list:
        payload += struct.pack('<i', val)

    tmp_file = os.path.join(output_dir, f".{id_str}.bin.tmp")
    final_file = os.path.join(output_dir, f"{id_str}.bin")

    with open(tmp_file, 'wb') as f:
        f.write(payload)

    os.rename(tmp_file, final_file)

    symlink_path = os.path.join(output_dir, category, f"{id_str}.bin")
    if not os.path.exists(symlink_path):
        os.symlink(f"../{id_str}.bin", symlink_path)

if __name__ == "__main__":
    main()
EOF

    # Compile it into a standalone binary
    cd /tmp
    pyinstaller --onefile packager.py

    # Move the binary to the expected location and strip it
    mkdir -p /app
    cp dist/packager /app/dataset_packager
    strip /app/dataset_packager || true
    chmod +x /app/dataset_packager

    # Cleanup
    rm -rf /tmp/packager.py /tmp/build /tmp/dist /tmp/packager.spec

    # Setup user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user