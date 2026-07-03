apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest numpy scipy

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/protein.pdb
ATOM      1  N   ALA A   1      10.123  12.345  15.678  1.00 10.00           N  
ATOM      2  CA  ALA A   1      11.234  13.456  16.789  1.00 10.00           C  
ATOM      3  C   ALA A   1      12.345  14.567  17.890  1.00 10.00           C  
ATOM      4  O   ALA A   1      13.456  15.678  18.901  1.00 10.00           O  
ATOM      5  N   GLY A   2      14.567  16.789  19.012  1.00 10.00           N  
ATOM      6  CA  GLY A   2      15.678  17.890  20.123  1.00 10.00           C  
ATOM      7  C   GLY A   2      16.789  18.901  21.234  1.00 10.00           C  
ATOM      8  O   GLY A   2      17.890  20.012  22.345  1.00 10.00           O  
ATOM      9  N   LEU A   3      18.901  21.123  23.456  1.00 10.00           N  
ATOM     10  CA  LEU A   3      20.012  22.234  24.567  1.00 10.00           C  
ATOM     11  C   LEU A   3      21.123  23.345  25.678  1.00 10.00           C  
ATOM     12  O   LEU A   3      22.234  24.456  26.789  1.00 10.00           O  
ATOM     13  N   VAL A   4      23.345  25.567  27.890  1.00 10.00           N  
ATOM     14  CA  VAL A   4      24.456  26.678  28.901  1.00 10.00           C  
EOF

    chmod -R 777 /home/user