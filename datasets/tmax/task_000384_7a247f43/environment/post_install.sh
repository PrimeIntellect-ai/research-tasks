apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scipy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/graph.csv
0,1,0,0,0,1
1,0,1,0,0,0
0,1,0,1,0,0
0,0,1,0,1,0
0,0,0,1,0,1
1,0,0,0,1,0
EOF

    cat << 'EOF' > /home/user/initial.csv
10.0
0.0
0.0
0.0
0.0
0.0
EOF

    chmod -R 777 /home/user