apt-get update && apt-get install -y python3 python3-pip gcc gdb strace ffmpeg fonts-liberation
    pip3 install pytest

    mkdir -p /app /home/user/src /home/user/logs /home/user/dumps

    # Create oracle
    cat << 'EOF' > /app/oracle_seq.c
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if(argc != 3) return 1;
    long start = atol(argv[1]);
    long len = atol(argv[2]);
    for(long i = 0; i < len; i++) {
        long n = start + i;
        printf("%ld ", (n*n*n) + 2);
    }
    printf("\n");
    return 0;
}
EOF
    gcc -o /app/oracle_seq /app/oracle_seq.c

    # Generate video
    ffmpeg -f lavfi -i color=c=black:s=320x240:d=3 -vf "drawtext=text='Result\: 3 10 29 66 127':fontcolor=white:fontsize=24:x=(w-text_w)/2:y=(h-text_h)/2" -pix_fmt yuv420p /app/crash_screen.mp4

    # Create buggy source code
    cat << 'EOF' > /home/user/src/math_seq.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main(int argc, char **argv) {
    if(argc != 3) return 1;

    FILE *f = fopen("/etc/math_seq.conf", "r");
    if(!f) {
        printf("Missing config\n");
        abort();
    }
    fclose(f);

    char *magic = getenv("INIT_MAGIC");
    if(!magic || strcmp(magic, "X9A2vPqL4mN7bK1w") != 0) {
        printf("Bad magic\n");
        abort();
    }

    long start = atol(argv[1]);
    long len = atol(argv[2]);
    for(long i = 0; i < len; i++) {
        long n = start + i;
        printf("%ld ", (long)pow(n, 3) + 2*n);
    }
    printf("\n");
    return 0;
}
EOF

    # Create strace log
    cat << 'EOF' > /home/user/logs/crash_strace.log
execve("./math_seq", ["./math_seq", "1", "5"], 0x7ffd0b0b0b00 /* 20 vars */) = 0
openat(AT_FDCWD, "/etc/math_seq.conf", O_RDONLY) = -1 ENOENT (No such file or directory)
--- SIGABRT {si_signo=SIGABRT, si_code=SI_TKILL, si_pid=1042, si_uid=1000} ---
+++ killed by SIGABRT (core dumped) +++
EOF

    # Create dummy core dump
    dd if=/dev/zero of=/home/user/dumps/core.math_seq.1042 bs=1k count=10
    echo "INIT_MAGIC=X9A2vPqL4mN7bK1w" >> /home/user/dumps/core.math_seq.1042

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app