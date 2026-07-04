apt-get update && apt-get install -y python3 python3-pip nginx git tzdata
    pip3 install pytest dateparser==1.1.8

    # Create vendored package
    mkdir -p /app/vendor
    git clone --depth 1 -b v1.1.8 https://github.com/scrapinghub/dateparser.git /app/vendor/dateparser

    # Introduce perturbation
    sed -i 's/import datetime/import datatime/' /app/vendor/dateparser/dateparser/conf.py

    # Create Oracle
    mkdir -p /app/oracle
    cat << 'EOF' > /app/oracle/log_converter_oracle
#!/usr/bin/env python3
import sys
import dateparser

if len(sys.argv) != 3:
    print("INVALID_DATE")
    sys.exit(1)

timestamp = sys.argv[1]
locale = sys.argv[2]

try:
    dt = dateparser.parse(timestamp, locales=[locale], settings={'TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True})
    if dt is None:
        print("INVALID_DATE")
        sys.exit(1)
    print(dt.strftime("%Y-%m-%d %H:%M:%S UTC"))
except Exception:
    print("INVALID_DATE")
    sys.exit(1)
EOF
    chmod +x /app/oracle/log_converter_oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app