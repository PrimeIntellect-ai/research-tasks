apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install dependencies
    apt-get install -y ffmpeg tesseract-ocr fonts-dejavu-core expect netcat-openbsd socat

    # Create app directory
    mkdir -p /app

    # Create legacy router CLI tool
    cat << 'EOF' > /app/legacy_router_cli
#!/bin/bash
read -p "Username: " user
if [ "$user" != "admin" ]; then echo "Auth failed"; exit 1; fi
read -s -p "Password: " pass
echo
if [ "$pass" != "netops" ]; then echo "Auth failed"; exit 1; fi
read -p "Enter STABLE ports space-separated: " ports
if [ "$ports" == "4011 4022 4033" ]; then
    echo "SUCCESS: 4011,4022,4033" > /home/user/router.cfg
    echo "Configuration saved."
else
    echo "Invalid ports."
    exit 1
fi
EOF
    chmod +x /app/legacy_router_cli

    # Generate video fixture
    ffmpeg -f lavfi -i color=c=black:s=640x480:d=2 -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:fontsize=30:fontcolor=white:x=50:y=50:text='DEPLOYMENT STATUS\nNODE 1 (Port 4011) - STABLE\nNODE 2 (Port 4022) - STABLE\nNODE 3 (Port 4044) - FAILED\nNODE 4 (Port 4033) - STABLE'" -c:v libx264 /app/network_glitch.mp4

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user