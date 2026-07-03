apt-get update && apt-get install -y python3 python3-pip jq gawk sed coreutils
    pip3 install pytest

    mkdir -p /home/user/storage_meta
    mkdir -p /app

    python3 -c "
import wave, struct, math
with wave.open('/app/voicemail.wav', 'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    for i in range(44100):
        value = int(32767.0*math.cos(440.0*math.pi*float(i)/44100.0))
        data = struct.pack('<h', value)
        w.writeframesraw(data)
"

    cat << 'EOF' > /home/user/storage_meta/batch1.csv
file_id,filename,project_code,size_bytes
F001,data_01.bin,ALPHA-10,5000000
F002,data_02.bin,ZETA-99,4000000
F003,data_03.bin,BETA-22,1500000
EOF

    cat << 'EOF' > /home/user/storage_meta/batch2.json
[
  {"file_id": "F004", "filename": "data_04.bin", "project_code": "ZETA-99", "size_bytes": 6000000},
  {"file_id": "F005", "filename": "data_05.bin", "project_code": "GAMMA-05", "size_bytes": 2000000}
]
EOF

    cat << 'EOF' > /home/user/storage_meta/batch3.csv
file_id,filename,project_code,size_bytes
F006,data_06.bin,ALPHA-10,3500000
F007,data_07.bin,ZETA-99,2450000
EOF

    cat << 'EOF' > /home/user/storage_meta/batch4.json
[
  {"file_id": "F008", "filename": "data_08.bin", "project_code": "BETA-22", "size_bytes": 8000000}
]
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/storage_meta
    chmod -R 777 /home/user