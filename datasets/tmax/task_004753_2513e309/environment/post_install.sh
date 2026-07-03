apt-get update && apt-get install -y python3 python3-pip gcc binutils cron
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app
    cat << 'EOF' > /tmp/ingester.c
#include <stdio.h>
int main() {
    printf("Ready to ingest records with mask: [MASKED_PII_STRICT_v9]\n");
    return 0;
}
EOF
    gcc -O2 /tmp/ingester.c -o /app/record_ingester
    strip /app/record_ingester
    rm /tmp/ingester.c

    mkdir -p /home/user/incoming /home/user/processed
    chown -R user:user /home/user/incoming /home/user/processed

    chmod -R 777 /home/user