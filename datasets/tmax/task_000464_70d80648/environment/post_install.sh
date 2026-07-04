apt-get update && apt-get install -y python3 python3-pip ffmpeg espeak
pip3 install pytest

mkdir -p /app
espeak -w /app/project_dictation.wav "The database password is set to archive_master_2023 but we need to rotate it soon because it was committed to the legacy repo."

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app