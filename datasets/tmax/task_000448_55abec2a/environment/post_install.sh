apt-get update && apt-get install -y python3 python3-pip gcc libc6-dev libseccomp-dev
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/.ssh
    cat << 'EOF' > /home/user/.ssh/target_rsa
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACD7z/0X1X+x8r0C7y1F1QkM9L2qR+wX2YwY0d+tTj+T3QAAAJB/vL/8f7y/
/AAAAAtzc2gtZWQyNTUxOQAAACD7z/0X1X+x8r0C7y1F1QkM9L2qR+wX2YwY0d+tTj+T3Q
AAAED1M3i1sTzM4uL/rW2G2mZ5u7X/5G8bL6b7O8Q9e7wTdfvP/RfVf7HyvQLvLUXVCRz0
vapH7BfZjBjR361OP5PdAAAACW1vY2sta2V5AQ==
-----END OPENSSH PRIVATE KEY-----
EOF

    cat << 'EOF' > /home/user/sandbox.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <sys/syscall.h>
#include <stddef.h>
#include <sys/wait.h>

int main(int argc, char **argv) {
    if (argc < 2) return 1;

    pid_t pid = fork();
    if (pid == 0) {
        struct sock_filter filter[] = {
            BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
            BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, SYS_open, 0, 1),
            BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
            BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW)
        };
        struct sock_fprog prog = { .len = 4, .filter = filter };
        prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0);
        prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog);
        execvp(argv[1], &argv[1]);
        exit(1);
    }
    wait(NULL);
    return 0;
}
EOF

    gcc -o /home/user/sandbox /home/user/sandbox.c

    chmod -R 777 /home/user
    chmod 700 /home/user/.ssh
    chmod 600 /home/user/.ssh/target_rsa