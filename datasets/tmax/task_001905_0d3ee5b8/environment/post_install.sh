apt-get update && apt-get install -y python3 python3-pip imagemagick tesseract-ocr fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Create the thresholds image
    convert -background white -fill black -font DejaVu-Sans -pointsize 24 label:"PORT 8080 MAX 500\nPORT 9090 MAX 200\nPORT 3000 MAX 1000" /app/thresholds.png

    # Create the oracle processor
    cat << 'EOF' > /app/oracle_processor
#!/bin/bash
while read -r ip port duration; do
  if [ "$port" = "8080" ]; then
    if [ "$duration" -gt 500 ]; then echo "ALERT $ip $port $duration"; else echo "OK $ip $port $duration"; fi
  elif [ "$port" = "9090" ]; then
    if [ "$duration" -gt 200 ]; then echo "ALERT $ip $port $duration"; else echo "OK $ip $port $duration"; fi
  elif [ "$port" = "3000" ]; then
    if [ "$duration" -gt 1000 ]; then echo "ALERT $ip $port $duration"; else echo "OK $ip $port $duration"; fi
  else
    echo "UNKNOWN $ip $port $duration"
  fi
done
EOF
    chmod +x /app/oracle_processor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user