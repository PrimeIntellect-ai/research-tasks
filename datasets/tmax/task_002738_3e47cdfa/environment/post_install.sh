apt-get update && apt-get install -y python3 python3-pip ffmpeg
pip3 install pytest

mkdir -p /home/user/docs
cat << 'EOF' > /home/user/docs/raw_notes.txt
[00:02] The system boots up and shows the initialization screen.
[00:06] The user navigates to the main configuration menu.
[00:12] Network settings are opened.
[00:15] IP address is configured.
[00:18] Changes are saved and applied.
[00:22] A confirmation dialog appears.
[00:25] The system reboots.
EOF

mkdir -p /app
ffmpeg -f lavfi -i testsrc=duration=30:size=640x480:rate=30 -pix_fmt yuv420p /app/screen_demo.mp4 2>/dev/null

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app