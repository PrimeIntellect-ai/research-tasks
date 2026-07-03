apt-get update && apt-get install -y python3 python3-pip g++ libomp-dev
pip3 install pytest

mkdir -p /home/user

cat << 'EOF' > /home/user/input.fasta
>seq1
ATGCGT
>seq2
ATGGGG
>seq3
CCCCAA
>seq4
CAATTT
>seq5
GGGGGG
EOF

cat << 'EOF' > /home/user/expected_stats.txt
Components: 2
Largest_Component_Size: 3
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user