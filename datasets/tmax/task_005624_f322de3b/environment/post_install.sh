apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest jsonschema
    pip3 install torch --index-url https://download.pytorch.org/whl/cpu

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import json
import torch
import torch.nn as nn
import random
import jsonschema

# Ensure reproducible setup
torch.manual_seed(42)
random.seed(42)

# 1. Create Model Weights
model = nn.Sequential(
    nn.Linear(5, 16),
    nn.ReLU(),
    nn.Linear(16, 2)
)
torch.save(model.state_dict(), '/home/user/model_weights.pt')

# 2. Create JSON Schema
schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "input": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 5,
            "maxItems": 5
        }
    },
    "required": ["id", "input"],
    "additionalProperties": False
}
with open('/home/user/schema.json', 'w') as f:
    json.dump(schema, f)

# 3. Create Dataset
valid_count = 0
with open('/home/user/raw_data.jsonl', 'w') as f:
    for i in range(1000):
        if random.random() < 0.8:
            # Valid row
            row = {"id": i, "input": [random.uniform(-1, 1) for _ in range(5)]}
            valid_count += 1
        else:
            # Invalid row
            err_type = random.choice([1, 2, 3])
            if err_type == 1:
                row = {"id": i} # missing input
            elif err_type == 2:
                row = {"id": i, "input": [1.0, 2.0]} # wrong length
            else:
                row = {"id": i, "input": [0.0]*5, "extra": "bad"} # extra property
        f.write(json.dumps(row) + "\n")

# Calculate expected outputs for verification
valid_inputs = []
with open('/home/user/raw_data.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        try:
            jsonschema.validate(instance=data, schema=schema)
            valid_inputs.append(data['input'])
        except jsonschema.exceptions.ValidationError:
            pass

input_tensor = torch.tensor(valid_inputs, dtype=torch.float32)
with torch.no_grad():
    model.eval()
    outputs = model(input_tensor)
    sum_dim0 = outputs[:, 0].sum().item()

with open('/home/user/ground_truth.json', 'w') as f:
    json.dump({
        "valid_samples": len(valid_inputs),
        "sum_output_dim0": round(sum_dim0, 4)
    }, f)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user