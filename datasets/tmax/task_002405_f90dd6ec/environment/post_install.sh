apt-get update && apt-get install -y python3 python3-pip ffmpeg tar sed util-linux libc-bin gawk
pip3 install pytest

mkdir -p /app
ffmpeg -f lavfi -i "color=c=red:s=320x240:d=1" \
       -f lavfi -i "color=c=blue:s=320x240:d=1" \
       -f lavfi -i "color=c=green:s=320x240:d=1" \
       -f lavfi -i "color=c=yellow:s=320x240:d=1" \
       -f lavfi -i "color=c=black:s=320x240:d=1" \
       -filter_complex "[0:v][1:v][2:v][3:v][4:v]concat=n=5:v=1[v]" \
       -map "[v]" -c:v libx264 -pix_fmt yuv420p /app/deploy_logs.mp4

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user