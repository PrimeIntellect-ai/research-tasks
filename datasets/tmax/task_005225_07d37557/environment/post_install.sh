apt-get update && apt-get install -y python3 python3-pip ffmpeg
pip3 install pytest SpeechRecognition

mkdir -p /app /home/user/docs
cd /app

# Create mock documentation files
echo "# API Details" > api.md
echo "# Auth Flow" > auth.md
echo "# Setup Guide" > setup.md
tar -czf docs.tar.gz api.md auth.md setup.md
rm api.md auth.md setup.md

# Create multi-line log file
cat << 'EOF' > edit_history.log
Commit: a1b2c3d
Date: 2023-01-15 10:00:00
File: api.md
Notes: Updated endpoints
---
Commit: e5f6g7h
Date: 2023-10-20 14:30:00
File: auth.md
Notes: Added notes on security
---
Commit: i8j9k0l
Date: 2023-05-12 09:15:00
File: setup.md
Notes: Fixed typo
EOF

# Create dummy dictation file for initial tests (will be mounted over by test runner)
touch /app/dictation.wav

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app