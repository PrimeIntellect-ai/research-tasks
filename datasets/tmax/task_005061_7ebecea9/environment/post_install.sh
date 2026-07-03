apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        imagemagick \
        fonts-dejavu-core \
        gcc \
        binutils \
        openssl

    pip3 install pytest

    # 1. Create video file
    mkdir -p /app
    # Fix Imagemagick policy if needed
    sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/g' /etc/ImageMagick-6/policy.xml || true
    convert -size 1024x768 xc:black -font DejaVu-Sans -pointsize 24 -fill white -draw "text 50,50 'curl -X POST -F \"file=@payload.elf\" -F \"path=../../uploads/sys_updater.elf\" http://target/upload'" /tmp/frame.png
    ffmpeg -loop 1 -i /tmp/frame.png -c:v libx264 -t 10 -pix_fmt yuv420p -vf "fps=30" /app/breach_capture.mp4

    # 2. Create ELF binary with custom section
    mkdir -p /var/www/uploads
    echo "int main() { return 0; }" > /tmp/elf.c
    gcc /tmp/elf.c -o /var/www/uploads/sys_updater.elf
    echo -n -e '\x1a\x0b' > /tmp/bk_port.bin
    objcopy --add-section .bk_port=/tmp/bk_port.bin /var/www/uploads/sys_updater.elf

    # 3. Create dummy files and manifest, alter permissions
    mkdir -p /var/www/config
    echo "dummy content" > /var/www/index.html
    echo "settings content" > /var/www/config/settings.yml
    cd /var/www
    sha256sum index.html config/settings.yml > /app/manifest.sha256
    chmod 0777 /var/www/config/settings.yml
    cd /

    # 4. Create rogue TLS certificate
    mkdir -p /etc/ssl/certs
    openssl req -x509 -newkey rsa:2048 -keyout /tmp/key.pem -out /etc/ssl/certs/rogue.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=EvilCorp/CN=EvilCorp Root CA"

    # 5. Create oracle sanitizer
    cat << 'EOF' > /app/oracle_sanitizer.py
import sys
path = sys.stdin.read()
print(path.replace('../', ''), end='')
EOF
    cat << 'EOF' > /app/oracle_sanitizer
#!/bin/bash
python3 /app/oracle_sanitizer.py "$@"
EOF
    chmod +x /app/oracle_sanitizer

    # 6. Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user