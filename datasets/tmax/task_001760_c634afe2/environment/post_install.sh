apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas

    mkdir -p /home/user/data
    mkdir -p /home/user/output

    cat << 'EOF' > /home/user/data/metadata.csv
doc_id,author,category
9007199254740993,Alice,Science
9007199254740995,,Math
9007199254740997,Bob,Physics
9007199254740999,Carol,
EOF

    cat << 'EOF' > /home/user/data/corpus.jsonl
{"doc_id": 9007199254740993, "text": "The quick brown fox"}
{"doc_id": 9007199254740995, "text": "jumps over the lazy dog"}
{"doc_id": 9007199254740997, "text": "hello world from physics the quick"}
{"doc_id": 9007199254740999, "text": "no category text quick"}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user