apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/points_A.csv
id_A,x,y,z
a1,1.04,2.01,3.05
a2,1.01,1.98,3.06
a3,5.00,5.00,5.00
a4,-1.55,2.44,-3.11
a5,-1.56,2.44,-3.11
EOF

    cat << 'EOF' > /home/user/points_B.csv
id_B,x,y,z
b1,1.02,1.99,3.14
b2,9.90,9.90,9.90
b3,5.01,4.96,5.04
b4,-1.55,2.39,-3.09
b5,1.02,1.99,3.14
EOF

    chmod -R 777 /home/user