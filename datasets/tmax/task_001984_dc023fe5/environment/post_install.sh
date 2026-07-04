apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/dataset

# Run 001
echo '{"exp_id": "EXP-X99", "operator": "Dr.Smith"}' | iconv -f UTF-8 -t UTF-16LE > /home/user/dataset/meta_001.json
cat << 'EOF' > /home/user/dataset/run_001.gcode
G21 ; Set units to mm
G90 ; Absolute positioning
G0 X0 Y0 Z5.0
G1 X10 Y10 Z-1.5 F100
G1 X20 Y10 Z-1.5
G0 Z12.4
G0 X0 Y0
EOF
echo "time,sensor1,sensor2" > /home/user/dataset/data_001.csv
echo "0.1,45,23" >> /home/user/dataset/data_001.csv

# Run 002
echo '{"exp_id": "EXP-Y42", "operator": "Alice"}' | iconv -f UTF-8 -t ISO-8859-1 > /home/user/dataset/meta_002.json
cat << 'EOF' > /home/user/dataset/run_002.gcode
G21
G90
G0 X15 Y15 Z10.0
G1 Z-5.0 F50
G1 X25 Y25 Z-5.0
G0 Z22.1
G0 X0 Y0
EOF
echo "time,sensor1,sensor2" > /home/user/dataset/data_002.csv
echo "0.1,41,25" >> /home/user/dataset/data_002.csv

# Run 003
echo '{"exp_id": "EXP-Z01", "operator": "Bob"}' > /home/user/dataset/meta_003.json
cat << 'EOF' > /home/user/dataset/run_003.gcode
G21
G0 X5 Y5 Z2.0
G1 X10 Y10 Z0.0
G1 X15 Y15 Z-10.0
G0 Z8.5
EOF
echo "time,sensor1,sensor2" > /home/user/dataset/data_003.csv
echo "0.1,39,28" >> /home/user/dataset/data_003.csv

chmod -R 777 /home/user