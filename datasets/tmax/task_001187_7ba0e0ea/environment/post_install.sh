apt-get update && apt-get install -y python3 python3-pip ffmpeg espeak-ng g++ pocketsphinx
    pip3 install pytest

    mkdir -p /app

    # Generate the audio file
    espeak-ng -w /app/incident_094.wav "Here are the updated dashboard normalization rules. Read the stream of metric pairs. If the subsystem is exactly NETWORK, drop the event completely. If the subsystem is exactly DISK, divide the metric value by two using integer division. If the subsystem is exactly CPU, add fifteen to the metric value. For any other subsystem, leave the metric value unchanged. Format the output by printing the subsystem, a colon, and the value, with each event on a new line."

    # Create and compile the oracle parser
    cat << 'EOF' > /app/oracle_parser.cpp
#include <iostream>
#include <string>

int main() {
    std::string subsystem;
    int value;
    while (std::cin >> subsystem >> value) {
        if (subsystem == "NETWORK") {
            continue;
        } else if (subsystem == "DISK") {
            value /= 2;
        } else if (subsystem == "CPU") {
            value += 15;
        }
        std::cout << subsystem << ":" << value << "\n";
    }
    return 0;
}
EOF
    g++ -O3 /app/oracle_parser.cpp -o /app/oracle_parser
    chmod +x /app/oracle_parser

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user