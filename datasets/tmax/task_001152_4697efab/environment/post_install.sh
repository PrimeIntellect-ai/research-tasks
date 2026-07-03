apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/input.fasta
>Strain_A
ATGCGTA
>Strain_B
GCGCGCGCGC
>Strain_C
ATATATATAT
EOF

    chmod -R 777 /home/user