apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc build-essential
    pip3 install pytest

    mkdir -p /app

    # Create the sanitizer oracle
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

void url_decode(char *dst, const char *src) {
    char a, b;
    while (*src) {
        if ((*src == '%') &&
            ((a = src[1]) && (b = src[2])) &&
            (isxdigit(a) && isxdigit(b))) {
            if (a >= 'a') a -= 'a'-'A';
            if (a >= 'A') a -= ('A' - 10);
            else a -= '0';
            if (b >= 'a') b -= 'a'-'A';
            if (b >= 'A') b -= ('A' - 10);
            else b -= '0';
            *dst++ = 16*a+b;
            src+=3;
        } else if (*src == '+') {
            *dst++ = ' ';
            src++;
        } else {
            *dst++ = *src++;
        }
    }
    *dst = '\0';
}

void remove_traversal(char *str) {
    int changed = 1;
    while (changed) {
        changed = 0;
        char *p = str;
        while ((p = strstr(p, "../")) != NULL) {
            memmove(p, p + 3, strlen(p + 3) + 1);
            changed = 1;
        }
        p = str;
        while ((p = strstr(p, "..\\")) != NULL) {
            memmove(p, p + 3, strlen(p + 3) + 1);
            changed = 1;
        }
    }
}

int main() {
    char line[4096];
    char extracted[4096] = {0};
    int found = 0;
    while (fgets(line, sizeof(line), stdin)) {
        char *lower_line = strdup(line);
        for(int i=0; lower_line[i]; i++) lower_line[i] = tolower(lower_line[i]);
        char *p = strstr(lower_line, "upload-path: ");
        if (p) {
            int offset = (p - lower_line) + 13;
            strcpy(extracted, line + offset);
            found = 1;
            free(lower_line);
            break;
        }
        free(lower_line);
    }
    if (found) {
        char *nl = strpbrk(extracted, "\r\n");
        if (nl) *nl = '\0';
        char decoded[4096];
        url_decode(decoded, extracted);
        remove_traversal(decoded);
        printf("%s", decoded);
    }
    return 0;
}
EOF
    gcc -O2 /tmp/oracle.c -o /app/sanitizer_oracle
    strip /app/sanitizer_oracle
    rm /tmp/oracle.c

    # Create the incident record video
    # We use drawtext filter in ffmpeg. To ensure it works, we need fonts, or we can just draw text simply.
    # Alternatively, we can use an image and convert it to video.
    apt-get install -y fonts-liberation
    echo "Upload-Path: ..%2f..%2f..%2fetc%2fshadow" > /tmp/payload.txt
    ffmpeg -f lavfi -i "color=c=black:s=640x480:d=5" -vf "drawtext=textfile=/tmp/payload.txt:fontcolor=white:fontsize=24:x=10:y=10" -c:v libx264 /app/incident_record.mp4
    rm /tmp/payload.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user