apt-get update && apt-get install -y python3 python3-pip tesseract-ocr gcc imagemagick fonts-dejavu-core

pip3 install --default-timeout=100 pytest

mkdir -p /app
# Generate the diagram image
convert -size 400x100 xc:white -font DejaVu-Sans -pointsize 36 -fill black -draw "text 10,50 'AEROLITH'" /app/diagram.png

# Create the oracle C program
cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    char *path = argv[1];
    char *base = strrchr(path, '/');
    if (base) {
        base++;
    } else {
        base = path;
    }
    printf("AEROLITH_");
    for (int i = strlen(base) - 1; i >= 0; i--) {
        putchar(base[i]);
    }
    return 0;
}
EOF

gcc -o /app/oracle_name_obfuscator /app/oracle.c
rm /app/oracle.c

# Create user directories and systemd service file
mkdir -p /home/user/.config/systemd/user
cat << 'EOF' > /home/user/.config/systemd/user/obfuscate-backup.service
[Unit]
Description=Obfuscate Backup Service

[Service]
Type=oneshot
ExecStart=/home/user/backup/name_obfuscator /var/log/syslog
EOF

mkdir -p /home/user/backup

useradd -m -s /bin/bash user || true
chown -R user:user /home/user
chmod -R 777 /home/user