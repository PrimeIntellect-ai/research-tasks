apt-get update && apt-get install -y python3 python3-pip ffmpeg netcat-openbsd socat jq gawk
pip3 install pytest

mkdir -p /app
cat << 'EOF' > /tmp/subs.srt
1
00:00:00,000 --> 00:00:01,000
SELECT emp_id, first_name, last_name, dept_id FROM employees WHERE emp_id = 5;

2
00:00:01,000 --> 00:00:02,000
INSERT INTO departments (dept_id, dept_name, location) VALUES (1, 'Engineering', 'NY');

3
00:00:02,000 --> 00:00:03,000
SELECT p.project_id, p.project_name, e.emp_id FROM projects p JOIN employees e ON p.lead_id = e.emp_id;
EOF

ffmpeg -y -f lavfi -i color=c=black:s=128x128 -i /tmp/subs.srt -c:v libx264 -c:s mov_text -t 3 /app/db_recording.mp4
rm /tmp/subs.srt

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user