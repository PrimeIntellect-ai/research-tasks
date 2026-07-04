apt-get update && apt-get install -y python3 python3-pip git build-essential
    pip3 install pytest

    mkdir -p /app /verify
    cd /app
    git clone https://github.com/facebookresearch/fastText.git
    cd fastText
    git checkout v0.9.2

    # Temporarily install fastText to train the model
    pip3 install .

    # Train the dummy model
    cat << 'EOF' > /tmp/train_model.py
import fasttext
with open("/tmp/train.txt", "w") as f:
    f.write("__label__keep this is good clean text\n")
    f.write("__label__discard 12938 1239128 bad text\n")
    f.write("__label__keep another valid text string\n")
    f.write("__label__discard xyz qqqq invalid noise\n")
model = fasttext.train_supervised("/tmp/train.txt")
model.save_model("/app/cleaner_model.bin")
EOF
    python3 /tmp/train_model.py

    # Uninstall fasttext so the agent must fix and install it
    pip3 uninstall -y fasttext

    # Perturb the setup.py
    sed -i 's/-std=c++11/-std=c89/g' /app/fastText/setup.py

    # Create the oracle script
    cat << 'EOF' > /verify/oracle_filter.py
#!/usr/bin/env python3
import sys
import re
import fasttext

model = fasttext.load_model('/app/cleaner_model.bin')

for line in sys.stdin:
    original_line = line.strip('\n')
    # Preprocess
    processed = re.sub(r'[^a-z ]', '', original_line.lower())
    if not processed.strip():
        continue
    labels, probs = model.predict(processed)
    if labels[0] == '__label__keep' and probs[0] >= 0.60:
        print(original_line)
EOF
    chmod +x /verify/oracle_filter.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user