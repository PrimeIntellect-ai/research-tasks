apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy

    # Create vendored package directory
    mkdir -p /app/vendored/tok_speed

    # Create setup.py with intentional typo
    cat << 'EOF' > /app/vendored/tok_speed/setup.py
from setuptools import setup, find_packages

setup(
    name='tok_speed',
    version='1.0.0',
    packages=find_packags(),
    py_modules=['tok_speed'],
)
EOF

    # Create tok_speed.py
    cat << 'EOF' > /app/vendored/tok_speed/tok_speed.py
def tokenize(text):
    return text.split()
EOF

    # Create data directories
    mkdir -p /app/data/clean
    mkdir -p /app/data/evil

    # Create clean data files (median token lengths ~4-5)
    cat << 'EOF' > /app/data/clean/doc1.txt
This is a normal English sentence.
EOF

    cat << 'EOF' > /app/data/clean/doc2.txt
The quick brown fox jumps over the lazy dog.
EOF

    cat << 'EOF' > /app/data/clean/doc3.txt
Data science is an interesting field with many applications.
EOF

    # Create evil data files (median token lengths > 8)
    cat << 'EOF' > /app/data/evil/doc1.txt
abcdefgh ijklmnop qrstuvwx yzabcdef ghijklmn
EOF

    cat << 'EOF' > /app/data/evil/doc2.txt
obfuscated adversarial documents contain abnormally lengthy tokens
EOF

    cat << 'EOF' > /app/data/evil/doc3.txt
supercalifragilisticexpialidocious pseudopseudohypoparathyroidism
EOF

    # Create user
    useradd -m -s /bin/bash user || true

    # Ensure /home/user is writable
    chmod -R 777 /home/user