apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tesseract-ocr \
        valgrind \
        g++-aarch64-linux-gnu \
        cmake \
        make

    pip3 install pytest

    mkdir -p /app
    touch /app/design_spec.png
    touch /app/oracle_analyzer_cli
    chmod +x /app/oracle_analyzer_cli

    mkdir -p /home/user/build_analyzer/src
    touch /home/user/build_analyzer/src/scoring.cpp
    touch /home/user/build_analyzer/src/graph.cpp
    touch /home/user/build_analyzer/src/api.cpp
    touch /home/user/build_analyzer/CMakeLists.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user