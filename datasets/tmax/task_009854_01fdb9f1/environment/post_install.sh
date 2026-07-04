apt-get update && apt-get install -y python3 python3-pip python3-venv
    pip3 install pytest

    # Create user
    useradd -m -s /bin/bash user || true

    # Create app directory
    mkdir -p /home/user/app

    # Create the python script
    cat << 'EOF' > /home/user/app/process_data.py
import sys
import json

try:
    import numpy as np
    import pandas as pd
except ImportError:
    print("Dependency conflict: require numpy 1.24.3 and pandas 2.0.3")
    sys.exit(1)

if np.__version__ != '1.24.3' or pd.__version__ != '2.0.3':
    print("Dependency conflict: require numpy 1.24.3 and pandas 2.0.3")
    sys.exit(1)

# Generate memory dump
with open('/home/user/app/memory.dmp', 'wb') as f:
    f.write(b'\x00\x01\x02' * 5000)
    f.write(b'ERROR_STATE_INIT\n')
    f.write(b'DIAG_TOKEN_X7K9M2Q4\n')
    f.write(b'\x03\x04\x05' * 5000)

# Generate output data with a deliberate mismatch at id 73
data = []
for i in range(1, 101):
    if i == 73:
        data.append({"id": i, "matrix": [1, 0, 0, 1]})
    else:
        data.append({"id": i, "matrix": [1, 0, 0, 0]})

with open('/home/user/app/output_data.json', 'w') as f:
    json.dump(data, f)

print("Processing complete. memory.dmp and output_data.json generated.")
EOF

    # Generate expected_data.json
    python3 -c '
import json
import os
data = [{"id": i, "matrix": [1, 0, 0, 0]} for i in range(1, 101)]
with open("/home/user/app/expected_data.json", "w") as f:
    json.dump(data, f)
'

    chown -R user:user /home/user/app
    chmod -R 777 /home/user