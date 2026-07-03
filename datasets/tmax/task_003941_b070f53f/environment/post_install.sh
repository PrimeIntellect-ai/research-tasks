apt-get update && apt-get install -y python3 python3-pip iproute2 cron gcc ffmpeg
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    touch /app/loc_updates.wav

    cat << 'EOF' > /home/user/historical.csv
timestamp,language,key,value
1600000000,en,welcome,Welcome
1600000000,fr,welcome,Bienvenue
1600000100,fr,welcome,Bienvenue!
1600000000,en,logout,Log out
1600000200,en,logout,Sign out
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app