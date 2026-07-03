apt-get update && apt-get install -y python3 python3-pip gcc make ffmpeg imagemagick
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user/url_router

    # Build oracle
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#define CONSTRAINT_MODULUS 204

void parse_url(const char *url, char *dest) {
    int i = 0;
    while (*url) { dest[i++] = *url++; }
    dest[i] = '\0';
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    char dest[256] = {0};
    parse_url(argv[1], dest);
    int sum = 0;
    for (int j = 0; dest[j]; j++) {
        sum += dest[j];
    }
    printf("ID: %d\n", sum % CONSTRAINT_MODULUS);
    return 0;
}
EOF
    gcc -o /app/oracle_router /tmp/oracle.c
    chmod +x /app/oracle_router

    # Create video
    mkdir -p /tmp/frames
    for i in $(seq 1 42); do
        convert -size 64x64 xc:red /tmp/frames/frame_$(printf "%03d" $i).png
    done
    for i in $(seq 43 100); do
        convert -size 64x64 xc:black /tmp/frames/frame_$(printf "%03d" $i).png
    done
    ffmpeg -framerate 10 -i /tmp/frames/frame_%03d.png -c:v libx264 -pix_fmt yuv420p /app/signal.mp4
    rm -rf /tmp/frames

    # Create buggy project
    cat << 'EOF' > /home/user/url_router/parser.h
#include <router.h>
#define CONSTRAINT_MODULUS 100
void parse_url(const char *url, char *dest);
EOF

    cat << 'EOF' > /home/user/url_router/router.h
#include <parser.h>
void route(const char *url);
EOF

    cat << 'EOF' > /home/user/url_router/parser.c
#include <parser.h>
void parse_url(const char *url, char *dest) {
    int i; 
    while (*url) { dest[i++] = *url++; }
    dest[i] = '\0';
}
EOF

    cat << 'EOF' > /home/user/url_router/main.c
#include <stdio.h>
#include <parser.h>

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    char dest[256] = {0};
    parse_url(argv[1], dest);
    int sum = 0;
    for (int j = 0; dest[j]; j++) {
        sum += dest[j];
    }
    printf("ID: %d\n", sum % CONSTRAINT_MODULUS);
    return 0;
}
EOF

    cat << 'EOF' > /home/user/url_router/Makefile
router_bin: main.o
	gcc -o router_bin main.o

main.o: main.c
	gcc -c main.c

parser.o: parser.c
	gcc -c parser.c
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/url_router
    chmod -R 777 /home/user