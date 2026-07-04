apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest

    mkdir -p /home/user/tracker

    cat << 'EOF' > /home/user/raw_configs.csv
Timestamp,Server,Key,Value
1001,srv1,max_conns,100
1002,srv1,max_conns,100
1003,srv1,max_conns,"100
# updated"
1004,srv1,max_conns,"200
# updated"
1005,srv2,timeout,30s
1006,srv2,timeout,60s
1007,srv2,timeout,60s
1008,srv2,timeout,120s
1009,srv1,max_conns,"200
# updated"
1010,srv1,max_conns,"300
# fast"
EOF

    cat << 'EOF' > /home/user/expected_configs.csv
Timestamp,Server,Key,ValueHash,Drift,RollingAvg
1001,srv1,max_conns,5c7865c37021eb23177eebe756a1202e8633c77d4023eb2599c9afdf0434444c,0,3.00
1003,srv1,max_conns,0dc9073dc0a0684f04c643b0185ec43d043d8333efc60f279ab8eebc95e1e194,10,8.00
1004,srv1,max_conns,8151c86aeb214db2fb2ba8ccbbf72f3e82b7cae61bb22f8a48af9fcffb796d11,1,9.67
1005,srv2,timeout,e0dbb5a933f7c9e535e692ec79860b0dffae7e780dc3c1097e3a9cb712ff2ec4,0,3.00
1006,srv2,timeout,629f106f235b2e9e62af63d76e3b2e7ef6dc6631b0fc2521191564cdfc892c55,1,3.00
1008,srv2,timeout,6b5b180373abec4fcb65c2b380327fcdbfa6703b41d01191317d73c7fc01705e,2,3.33
1010,srv1,max_conns,58fbaea5428a2a7cc3097c2d7f8f6df746409b307ce4e4604e7ad183d3750ec1,8,12.00
EOF

    cat << 'EOF' > /home/user/verify.py
import csv
import sys

def normalize_rows(filename):
    try:
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f)
            # Filter out empty rows if any
            return [row for row in reader if row]
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []

expected = normalize_rows('/home/user/expected_configs.csv')
actual = normalize_rows('/home/user/processed_configs.csv')

if len(expected) != len(actual):
    print(f"Row count mismatch. Expected {len(expected)}, got {len(actual)}")
    sys.exit(1)

for i, (exp_row, act_row) in enumerate(zip(expected, actual)):
    if exp_row != act_row:
        print(f"Mismatch at row {i+1}:\nExpected: {exp_row}\nActual:   {act_row}")
        sys.exit(1)

print("Success")
sys.exit(0)
EOF
    chmod +x /home/user/verify.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user