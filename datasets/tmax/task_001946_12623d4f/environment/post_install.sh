apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    mkdir -p /home/user/investigation/

    cat << 'EOF' > /home/user/investigation/auth_service.cpp
#include <iostream>
#include <string>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <cstdlib>

using namespace std;

string get_secret_key() {
    ifstream keyfile("/etc/auth_secret.key");
    string key;
    if (keyfile.is_open()) {
        getline(keyfile, key);
        keyfile.close();
    } else {
        // Fallback for demonstration if missing
        key = "UNKNOWN"; 
    }
    return key;
}

string generate_token(const string& username, const string& key) {
    stringstream ss;
    for (size_t i = 0; i < username.length(); ++i) {
        unsigned char cipher = username[i] ^ key[i % key.length()];
        ss << hex << setfill('0') << setw(2) << (int)cipher;
    }
    return ss.str();
}

void validate_token(const string& username, const string& token) {
    string expected = generate_token(username, get_secret_key());
    if (token == expected) {
        cout << "Access Granted." << endl;
    } else {
        cout << "Access Denied." << endl;
        // Log the failed attempt
        string cmd = "echo 'Failed attempt for user: " + username + "' >> /tmp/auth.log";
        system(cmd.c_str());
    }
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cout << "Usage: " << argv[0] << " --validate <username> <token>" << endl;
        return 1;
    }

    string mode = argv[1];
    string username = argv[2];

    if (mode == "--validate" && argc == 4) {
        string token = argv[3];
        validate_token(username, token);
    }
    return 0;
}
EOF

    cat << 'EOF' > /home/user/investigation/intercepted_tokens.txt
alice : 12090a1100
bob : 110a01
eve : 0e1302
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user