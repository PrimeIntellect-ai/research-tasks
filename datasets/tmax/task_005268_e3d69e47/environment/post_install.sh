apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg
pip3 install pytest gTTS

mkdir -p /app

# Generate audio memo
python3 -c "
from gtts import gTTS
text = 'Hey, this is the dev lead. For the new log processor, skip the first twelve bytes, use a block size of sixty four, and xor everything with hexadecimal A three.'
tts = gTTS(text)
tts.save('/app/project_memo.mp3')
"
ffmpeg -i /app/project_memo.mp3 /app/project_memo.wav
rm /app/project_memo.mp3

# Create oracle C program
cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int magic = 12;
    unsigned char key = 0xA3;

    for (int i = 0; i < magic; i++) {
        if (fgetc(stdin) == EOF) return 0;
    }

    unsigned char buf[64];
    size_t n;
    while ((n = fread(buf, 1, 64, stdin)) > 0) {
        for (size_t i = 0; i < n; i++) {
            buf[i] ^= key;
        }
        fwrite(buf, 1, n, stdout);
    }
    return 0;
}
EOF

gcc /app/oracle.c -o /app/oracle_transformer
rm /app/oracle.c

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app