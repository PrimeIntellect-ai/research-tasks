apt-get update && apt-get install -y python3 python3-pip build-essential git wget ffmpeg
    pip3 install pytest gTTS

    mkdir -p /app
    mkdir -p /opt

    # Generate the audio memo
    python3 -c "from gtts import gTTS; tts = gTTS('Please write a parser that processes the multi-line sensor logs. We only care about extreme thermal events. Only extract records where the severity is either ERROR or FATAL, and the temperature is strictly greater than 45.0 degrees. For these matching records, print the EventID and the Temperature separated by a single tab character.'); tts.save('/tmp/memo.mp3')"
    ffmpeg -i /tmp/memo.mp3 -ar 16000 -ac 1 -c:a pcm_s16le /app/filter_memo.wav

    # Install whisper.cpp
    git clone https://github.com/ggerganov/whisper.cpp.git /opt/whisper.cpp
    cd /opt/whisper.cpp
    git checkout v1.5.4
    make
    bash ./models/download-ggml-model.sh base.en

    # Create the oracle parser
    cat << 'EOF' > /app/oracle_parser.cpp
#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string line;
    std::string event_id;
    std::string severity;
    double temperature = 0.0;
    bool has_temp = false;

    while (std::getline(std::cin, line)) {
        if (line == "---") {
            if ((severity == "ERROR" || severity == "FATAL") && has_temp && temperature > 45.0) {
                std::cout << event_id << "\t" << temperature << "\n";
            }
            event_id = "";
            severity = "";
            temperature = 0.0;
            has_temp = false;
        } else {
            if (line.find("EventID: ") == 0) event_id = line.substr(9);
            else if (line.find("Severity: ") == 0) severity = line.substr(10);
            else if (line.find("Temperature: ") == 0) {
                temperature = std::stod(line.substr(13));
                has_temp = true;
            }
        }
    }
    // handle final record if no trailing ---
    if (!event_id.empty() && (severity == "ERROR" || severity == "FATAL") && has_temp && temperature > 45.0) {
        std::cout << event_id << "\t" << temperature << "\n";
    }
    return 0;
}
EOF
    g++ -O3 /app/oracle_parser.cpp -o /app/oracle_parser
    chmod +x /app/oracle_parser

    # Create dummy sensor logs
    mkdir -p /app/dummy_logs
    cat << 'EOF' > /app/dummy_logs/log1.txt
EventID: 101
Severity: ERROR
Temperature: 50.5
Battery: 20.0%
Message: Thermal runaway
---
EventID: 102
Severity: INFO
Temperature: 25.0
Battery: 80.0%
Message: Normal operation
---
EOF
    cd /app/dummy_logs
    tar -czf /app/sensor_logs.tar.gz log1.txt
    rm -rf /app/dummy_logs

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user