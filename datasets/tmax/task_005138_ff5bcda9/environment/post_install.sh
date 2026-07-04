apt-get update && apt-get install -y python3 python3-pip build-essential git wget gcc ffmpeg
pip3 install pytest gTTS

# Build Whisper.cpp (using a specific version to ensure 'main' binary is built)
git clone https://github.com/ggerganov/whisper.cpp.git /opt/whisper_src
cd /opt/whisper_src
git checkout v1.5.0
make

mkdir -p /opt/whisper/models
cp main /opt/whisper/main
wget -O /opt/whisper/models/ggml-base.en.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin

mkdir -p /app

# Generate oracle C program
cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <string.h>

int main() {
    char buffer[1024];
    if (!fgets(buffer, sizeof(buffer), stdin)) return 0;
    int len = strlen(buffer);
    if (len > 0 && buffer[len-1] == '\n') {
        buffer[len-1] = '\0';
        len--;
    }

    // Step 1: Reverse
    for (int i = 0; i < len / 2; i++) {
        char temp = buffer[i];
        buffer[i] = buffer[len - 1 - i];
        buffer[len - 1 - i] = temp;
    }

    // Step 2: Replace
    for (int i = 0; i < len; i++) {
        if (buffer[i] == 'a') buffer[i] = '1';
        else if (buffer[i] == 'b') buffer[i] = '2';
        else if (buffer[i] == 'c') buffer[i] = '3';
    }

    printf("%s\n", buffer);
    return 0;
}
EOF
gcc -O3 /tmp/oracle.c -o /app/oracle_daemon
strip /app/oracle_daemon

# Generate voicemail audio file
python3 -c "
from gtts import gTTS
text = \"System failure recovery log. First, create the spool directory structure. In the user home folder, create a directory called 'spool'. Inside 'spool', create three directories: 'incoming', 'processed', and 'failed'. Next, create a symbolic link named 'data_in' in the user home directory that points to the 'incoming' folder. Now for the telemetry algorithm. The processor reads a string from standard input. Step one: completely reverse the entire string. Step two: replace all lowercase letter 'a' with the number '1', replace all lowercase letter 'b' with the number '2', and replace all lowercase letter 'c' with the number '3'. Output the result.\"
tts = gTTS(text)
tts.save('/app/voicemail.mp3')
"
# Whisper requires 16kHz WAV files
ffmpeg -i /app/voicemail.mp3 -ar 16000 -ac 1 -c:a pcm_s16le /app/voicemail.wav
rm /app/voicemail.mp3

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user