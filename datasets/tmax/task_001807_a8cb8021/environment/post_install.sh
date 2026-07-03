apt-get update && apt-get install -y python3 python3-pip gawk
pip3 install pytest

mkdir -p /app

# Create dummy voicemail.wav
touch /app/voicemail.wav

# Generate the leaked hash (must be exactly for "sysadmin4092" without newline)
echo -n "588ea285f5eef1411ee852ef7cf032fb7b69324b1a403ff2b9a7b931dc9150ab" > /app/leaked_hash.txt

# Create the raw logs
cat << 'EOF' > /app/raw_logs.json
{
  "events": [
    {
      "timestamp": "2023-10-01T12:00:00Z",
      "user_id": 101,
      "message": "User registered with SSN 123-45-6789 successfully."
    },
    {
      "timestamp": "2023-10-01T12:05:00Z",
      "user_id": 102,
      "message": "Payment processed for card 4000 1234 5678 9010."
    },
    {
      "timestamp": "2023-10-01T12:10:00Z",
      "user_id": 103,
      "message": "Standard login event. No sensitive data here."
    },
    {
      "timestamp": "2023-10-01T12:15:00Z",
      "user_id": 104,
      "message": "Updated profile for SSN 987-65-4321 and card 5555 0000 1111 2222."
    }
  ]
}
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app