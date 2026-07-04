apt-get update && apt-get install -y python3 python3-pip gcc binutils
    pip3 install pytest packaging

    mkdir -p /home/user/artifacts
    cd /home/user/artifacts

    # Create source files
    cat << 'EOF' > alpha.c
void insecure_legacy_auth() {}
EOF

    cat << 'EOF' > beta.c
void insecure_legacy_auth() {}
EOF

    cat << 'EOF' > gamma.c
void secure_auth() {}
EOF

    cat << 'EOF' > delta.c
void secure_auth() {}
EOF

    # Compile to shared libraries
    gcc -shared -fPIC alpha.c -o libalpha.so
    gcc -shared -fPIC beta.c -o libbeta.so
    gcc -shared -fPIC gamma.c -o libgamma.so
    gcc -shared -fPIC delta.c -o libdelta.so

    # Create the manifest
    echo "libalpha.so:1.2.4\nlibbeta.so:1.5.0\nlibgamma.so:1.4.9\nlibdelta.so:2.0.1" > manifest.txt
    base64 manifest.txt > manifest.b64
    rm manifest.txt *.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user