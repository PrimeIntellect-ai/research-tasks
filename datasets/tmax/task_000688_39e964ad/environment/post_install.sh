apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Ensure pip command is available for the tests
    if [ ! -f /usr/bin/pip ]; then
        ln -s /usr/bin/pip3 /usr/bin/pip
    fi

    # Create vendored package directory
    mkdir -p /app/text-sampler-0.5.0/text_sampler

    # Create setup.py with broken numpy dependency
    cat << 'EOF' > /app/text-sampler-0.5.0/setup.py
from setuptools import setup, find_packages

setup(
    name="text-sampler",
    version="0.5.0",
    packages=find_packages(),
    install_requires=["numpy==99.9.9"],
    entry_points={
        "console_scripts": [
            "text-sampler=text_sampler.cli:main"
        ]
    }
)
EOF

    # Create text_sampler/__init__.py
    touch /app/text-sampler-0.5.0/text_sampler/__init__.py

    # Create text_sampler/cli.py
    cat << 'EOF' > /app/text-sampler-0.5.0/text_sampler/cli.py
import argparse
import numpy as np
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--n", type=int, required=True)
    args = parser.parse_args()

    with open(args.file, "r") as f:
        lines = f.readlines()

    if not lines:
        return

    sampled = np.random.choice(lines, size=args.n, replace=True)
    for line in sampled:
        sys.stdout.write(line)

if __name__ == "__main__":
    main()
EOF

    # Create user and directories
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/corpora/clean
    mkdir -p /home/user/corpora/evil

    # Create clean files
    cat << 'EOF' > /home/user/corpora/clean/clean1.txt
SCHEMA_VERSION=1.0
This is a clean file.
It has valid ASCII characters.
No injects here.
EOF

    cat << 'EOF' > /home/user/corpora/clean/clean2.txt
SCHEMA_VERSION=1.0
Another clean file.
Just some text.
EOF

    cat << 'EOF' > /home/user/corpora/clean/clean3.txt
SCHEMA_VERSION=1.0
Third clean file.
Good to go.
EOF

    # Create evil files
    cat << 'EOF' > /home/user/corpora/evil/evil1.txt
This is an evil file.
Missing the schema version header.
EOF

    cat << 'EOF' > /home/user/corpora/evil/evil2.txt
SCHEMA_VERSION=1.0
This file has non-ASCII bytes.
Like this: ÿ
EOF

    cat << 'EOF' > /home/user/corpora/evil/evil3.txt
SCHEMA_VERSION=1.0
This file has an inject.
[INJECT] eval(something)
EOF

    # Set permissions
    chmod -R 777 /app
    chmod -R 777 /home/user