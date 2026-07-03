apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user/data/papers
    mkdir -p /app

    echo "author_id,name,institution" > /home/user/data/authors.csv
    echo "A1,Alice,MIT" >> /home/user/data/authors.csv

    echo '{"id": "P1", "title": "Paper 1", "year": 2015, "authors": ["A1"], "references": []}' > /home/user/data/papers/P1.json

    cat << 'EOF' > /app/citation_oracle
#!/bin/bash
# Dummy oracle
echo "{}" > "$3"
EOF
    chmod +x /app/citation_oracle

    echo "A1" > /home/user/queries.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app