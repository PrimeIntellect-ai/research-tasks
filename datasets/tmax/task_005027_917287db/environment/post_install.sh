apt-get update && apt-get install -y python3 python3-pip imagemagick tesseract-ocr libtesseract-dev tesseract-ocr-eng gcc
    pip3 install pytest

    # Fix ImageMagick policy if it restricts operations
    rm -f /etc/ImageMagick-6/policy.xml

    mkdir -p /app

    # Generate the rules image
    convert -background white -fill black -pointsize 24 -size 800x300 \
      caption:"MAPPING RULES:\n1. Bucket = (timestamp - 1609459200) / 3600\n2. UID = (user_id * 101) % 997\n3. Masked Email = First character of email + '***' + '@' + domain\n4. Val = value * 3.14 (print as %.2f)" \
      /app/rules.png

    # Create the oracle program
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char line[2048];
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        char buf[2048];
        strcpy(buf, line);

        char *t_str = strtok(buf, ",");
        char *u_str = strtok(NULL, ",");
        char *e_str = strtok(NULL, ",");
        char *v_str = strtok(NULL, ",");
        char *extra = strtok(NULL, ",");

        if (!t_str || !u_str || !e_str || !v_str || extra) continue;

        int len = strlen(e_str);
        if (len < 4) continue;
        if (strcmp(e_str + len - 4, ".edu") != 0 && strcmp(e_str + len - 4, ".com") != 0) continue;

        char *at = strchr(e_str, '@');
        if (!at || at == e_str || at == e_str + len - 1) continue;

        long long T = atoll(t_str);
        long long user_id = atoll(u_str);
        double value = atof(v_str);

        long long bucket = (T - 1609459200) / 3600;
        long long uid = (user_id * 101) % 997;

        char first_char = e_str[0];
        char *domain = at + 1;

        double val = value * 3.14;

        printf("%lld,%lld,%c***@%s,%.2f\n", bucket, uid, first_char, domain, val);
    }
    return 0;
}
EOF
    gcc -O3 /app/oracle.c -o /app/oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app