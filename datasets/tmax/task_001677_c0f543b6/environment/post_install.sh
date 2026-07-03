apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /home/user
    mkdir -p /app

    # Generate docs.pkg
    cat << 'EOF' > /home/user/make_pkg.py
import struct

def add_file(f, path, content):
    f.write(struct.pack('<B', len(path)))
    f.write(path.encode('utf-8'))
    f.write(struct.pack('<I', len(content)))
    f.write(content.encode('utf-8'))

with open('/home/user/docs.pkg', 'wb') as f:
    add_file(f, 'draft.txt', 'Documentation Draft v1.2\nNotes:\n[DICTATION_INSERT]\nEnd of notes.\n')
    add_file(f, '../evil.txt', 'This should not be extracted.')
    add_file(f, '/absolute_evil.txt', 'This should also not be extracted.')
    add_file(f, 'safe_image.bin', 'fake binary data')
EOF
    python3 /home/user/make_pkg.py
    rm /home/user/make_pkg.py

    # Create extractor.c
    cat << 'EOF' > /home/user/extractor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <archive.pkg> <out_dir>\n", argv[0]);
        return 1;
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) { perror("open"); return 1; }

    struct stat st;
    fstat(fd, &st);
    unsigned char *data = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);

    size_t offset = 0;
    while (offset < st.st_size) {
        unsigned char path_len = data[offset++];
        char path[256] = {0};
        memcpy(path, data + offset, path_len);
        offset += path_len;

        unsigned int content_len;
        memcpy(&content_len, data + offset, 4);
        offset += 4;

        char out_path[512];
        sprintf(out_path, "%s/%s", argv[2], path);

        // VULNERABILITY: No check on 'path' for "../" or leading "/"

        FILE *out = fopen(out_path, "wb");
        if (out) {
            fwrite(data + offset, 1, content_len, out);
            fclose(out);
        }

        offset += content_len;
    }

    munmap(data, st.st_size);
    close(fd);
    return 0;
}
EOF

    # Create a valid silent wav file to satisfy the initial state tests
    cat << 'EOF' > /app/make_wav.py
import wave
import struct

with wave.open('/app/doc_notes.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(16000)
    for _ in range(16000):
        f.writeframesraw(struct.pack('<h', 0))
EOF
    python3 /app/make_wav.py
    rm /app/make_wav.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app