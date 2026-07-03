apt-get update && apt-get install -y python3 python3-pip g++ ffmpeg
    pip3 install pytest gTTS

    # Create directories
    mkdir -p /app/data /app/bin
    mkdir -p /home/user

    # Generate audio fixture
    cat << 'EOF' > /tmp/gen_audio.py
from gtts import gTTS
import os

text = "The primary sequence is A U G G C U A A C G G U A C C U A A. Observation time is ten seconds."
tts = gTTS(text)
tts.save("/tmp/audio.mp3")
EOF
    python3 /tmp/gen_audio.py
    ffmpeg -i /tmp/audio.mp3 /app/data/lab_dictation.wav
    rm /tmp/gen_audio.py /tmp/audio.mp3

    # Create oracle program
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <string>
#include <iomanip>

int main(int argc, char* argv[]) {
    if (argc < 2) return 1;
    std::string seq = argv[1];
    // A dummy deterministic output to serve as the oracle for this setup
    double p1 = 0.5;
    double p2 = 0.5;
    std::cout << std::fixed << std::setprecision(4) << p1 << " " << p2 << std::endl;
    return 0;
}
EOF
    g++ -O3 /tmp/oracle.cpp -o /app/bin/oracle_rna_model
    rm /tmp/oracle.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app