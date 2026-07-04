apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick fonts-dejavu-core unzip zip g++
    pip3 install pytest

    mkdir -p /app

    # Generate the emergency password image
    convert -size 400x100 xc:white -font DejaVu-Sans -pointsize 24 -fill black -draw "text 10,50 'Secur3P@ssw0rd2024!'" /app/emergency_password.png

    # Create the oracle rotator source and compile it
    cat << 'EOF' > /app/oracle.cpp
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <sys/stat.h>
#include <unistd.h>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <username> <new_password_hash>" << endl;
        return 1;
    }

    struct stat st;
    if (fstat(STDIN_FILENO, &st) == 0) {
        if (S_ISREG(st.st_mode) && (st.st_mode & 077) != 0) {
            cout << "Error: Insecure permissions" << endl;
            return 1;
        }
    }

    string target_user = argv[1];
    string new_hash = argv[2];
    string line;
    while (getline(cin, line)) {
        size_t pos1 = line.find(':');
        if (pos1 != string::npos) {
            string user = line.substr(0, pos1);
            if (user == target_user) {
                size_t pos2 = line.find(':', pos1 + 1);
                if (pos2 != string::npos) {
                    cout << user << ":" << new_hash << line.substr(pos2) << endl;
                } else {
                    cout << user << ":" << new_hash << endl;
                }
            } else {
                cout << line << endl;
            }
        } else {
            cout << line << endl;
        }
    }
    return 0;
}
EOF
    g++ -O3 /app/oracle.cpp -o /app/oracle_rotator
    chmod +x /app/oracle_rotator

    # Create the legacy vulnerable source and zip it with a password
    cat << 'EOF' > /app/main.cpp
#include <iostream>
#include <string>
#include <cstring>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 3) return 1;
    char buffer[256];
    strcpy(buffer, argv[1]); // Vulnerable to buffer overflow

    string target_user = argv[1];
    string new_hash = argv[2];
    string line;
    while (getline(cin, line)) {
        size_t pos1 = line.find(':');
        if (pos1 != string::npos) {
            string user = line.substr(0, pos1);
            if (user == target_user) {
                size_t pos2 = line.find(':', pos1 + 1);
                if (pos2 != string::npos) {
                    cout << user << ":" << new_hash << line.substr(pos2) << endl;
                } else {
                    cout << user << ":" << new_hash << endl;
                }
            } else {
                cout << line << endl;
            }
        } else {
            cout << line << endl;
        }
    }
    return 0;
}
EOF
    cd /app
    zip -P "Secur3P@ssw0rd2024!" legacy_rotator.zip main.cpp
    rm main.cpp oracle.cpp

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user