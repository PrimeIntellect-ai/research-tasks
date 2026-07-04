apt-get update && apt-get install -y python3 python3-pip curl wget gawk procps
    pip3 install pytest

    mkdir -p /home/user/etl_source
    cd /home/user/etl_source

    cat << 'EOF' > raw_transactions.csv
tx_id,category,amount
101,Furniture,120.50
102,Electronics,299.99
103,Furniture,45.00
104,Clothing,15.99
105,Electronics,100.01
106,Toys,55.50
107,Clothing,24.01
108,Groceries,210.25
109,Groceries,89.75
110,Toys,14.50
EOF

    iconv -f UTF-8 -t UTF-16LE raw_transactions.csv > transactions.csv
    rm raw_transactions.csv

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user