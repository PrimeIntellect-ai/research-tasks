apt-get update && apt-get install -y python3 python3-pip cmake g++ make pkg-config libavcodec-dev libavformat-dev libavutil-dev libswscale-dev git ffmpeg
    pip3 install pytest

    mkdir -p /app
    touch /app/evidence.mp4

    mkdir -p /home/user/video_service/src
    mkdir -p /home/user/video_service/vendor

    cat << 'EOF' > /home/user/video_service/CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(VideoService)
set(CMAKE_CXX_STANDARD 17)
add_executable(server src/server.cpp src/analyzer.cpp)
target_link_directories(server PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/vendor)
target_link_libraries(server avcodec_stub)
EOF

    cat << 'EOF' > /home/user/video_service/src/analyzer.cpp
#include <iostream>
EOF

    cat << 'EOF' > /home/user/video_service/src/server.cpp
#include <iostream>
EOF

    cd /home/user/video_service
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"
    echo "AUTH_TOKEN=sec_r3t_v1d30_t0k3n" > config.ini
    git add config.ini
    git commit -m "Add config"
    rm config.ini
    git add config.ini
    git commit -m "Remove config accidentally"

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/video_service
    chmod -R 777 /home/user