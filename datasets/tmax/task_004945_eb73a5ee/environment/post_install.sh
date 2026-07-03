apt-get update && apt-get install -y python3 python3-pip git wget curl
pip3 install pytest

# Create directories
mkdir -p /app/vendored
mkdir -p /home/user/raw_locales
mkdir -p /home/user/fixed_locales
mkdir -p /app/golden_locales

# Download polib 1.1.1
cd /app/vendored
wget https://github.com/izimobil/polib/archive/refs/tags/1.1.1.tar.gz
tar -xzf 1.1.1.tar.gz
rm 1.1.1.tar.gz

# Apply perturbation
cd polib-1.1.1
sed -i "s/return 'utf-8'/return 'ascii'/g" polib.py
# Just in case, append a dummy function to ensure 'ascii' is in the file
echo "\ndef _dummy_fallback():\n    return 'ascii'\n" >> polib.py

# Install original polib for setup script
pip3 install polib==1.1.1

# Generate golden and corrupted locales
cat << 'EOF' > /tmp/setup_locales.py
import os
import polib

golden_dir = "/app/golden_locales"
raw_dir = "/home/user/raw_locales"

locales = {
    "es": [("Hello", "Hola"), ("The penguin jumped", "El pingüino saltó")],
    "fr": [("Hello", "Bonjour"), ("The penguin jumped", "Le pingouin a sauté")],
    "de": [("Hello", "Hallo"), ("The penguin jumped", "Der Pinguin sprang")]
}

for lang, translations in locales.items():
    # Golden
    po_golden = polib.POFile()
    po_golden.metadata = {'Content-Type': 'text/plain; charset=utf-8'}
    for msgid, msgstr in translations:
        entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
        po_golden.append(entry)
    po_golden.save(os.path.join(golden_dir, f"{lang}.po"))

    # Corrupted
    po_raw = polib.POFile()
    # No charset header
    for msgid, msgstr in translations:
        corrupted_str = msgstr.encode('utf-8').decode('latin-1')
        entry = polib.POEntry(msgid=msgid, msgstr=corrupted_str)
        po_raw.append(entry)
    po_raw.save(os.path.join(raw_dir, f"{lang}.po"))
EOF

python3 /tmp/setup_locales.py

# Create verification script
cat << 'EOF' > /app/verify_accuracy.py
import sys
import polib
import difflib
import glob
import os

def calculate_accuracy():
    golden_files = glob.glob('/app/golden_locales/*.po')
    total_ratio = 0.0
    count = 0

    for golden_path in golden_files:
        lang = os.path.basename(golden_path)
        agent_path = f'/home/user/fixed_locales/{lang}'

        if not os.path.exists(agent_path):
            print(f"Missing {agent_path}")
            sys.exit(1)

        golden_po = polib.pofile(golden_path, encoding='utf-8')
        agent_po = polib.pofile(agent_path, encoding='utf-8')

        for g_entry, a_entry in zip(golden_po, agent_po):
            ratio = difflib.SequenceMatcher(None, g_entry.msgstr, a_entry.msgstr).ratio()
            total_ratio += ratio
            count += 1

    avg_accuracy = total_ratio / count if count > 0 else 0
    print(f"Accuracy: {avg_accuracy:.4f}")

    if avg_accuracy >= 0.98:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    calculate_accuracy()
EOF

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app