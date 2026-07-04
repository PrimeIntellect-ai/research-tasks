apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /app
    touch /app/voicemail.wav

    cat << 'EOF' > /usr/local/bin/whisper
#!/bin/bash
echo 'Transcript: "Hi, please update the operator. We need the pods to run in the Pacific/Fiji timezone, and use the en_NZ.UTF-8 locale. Also, make sure the wrapper cron job redirects all output to /var/operator/manifest_logs. Thanks."'
EOF
    chmod +x /usr/local/bin/whisper

    cat << 'EOF' > /app/oracle_generator
#!/bin/bash
cat <<INNER_EOF
apiVersion: v1
kind: Pod
metadata:
  name: $1
  labels:
    app: operator-managed
spec:
  containers:
  - name: main
    image: alpine:latest
    env:
    - name: TZ
      value: "$2"
    - name: LANG
      value: "$3"
    command: ["sleep", "infinity"]
INNER_EOF
EOF
    chmod +x /app/oracle_generator

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user