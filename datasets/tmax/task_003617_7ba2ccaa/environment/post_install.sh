apt-get update && apt-get install -y python3 python3-pip git g++ espeak
pip3 install pytest

mkdir -p /app
espeak -w /app/alert.wav "Alert. The routing table monitor is failing. Please update the git hook environment to set log dir to slash home slash user slash netlogs."

cat << 'EOF' > /app/oracle_normalizer.cpp
#include <iostream>
#include <string>
#include <regex>
#include <iomanip>
#include <sstream>

using namespace std;

int main() {
    string input;
    if (!getline(cin, input)) return 0;

    regex r("^([1-9][0-9]{0,2}|0)\\.([1-9][0-9]{0,2}|0)\\.([1-9][0-9]{0,2}|0)\\.([1-9][0-9]{0,2}|0) (UP|DOWN)$");
    smatch match;
    if (regex_match(input, match, r)) {
        int a = stoi(match[1].str());
        int b = stoi(match[2].str());
        int c = stoi(match[3].str());
        int d = stoi(match[4].str());

        if (a <= 255 && b <= 255 && c <= 255 && d <= 255) {
            char buffer[64];
            snprintf(buffer, sizeof(buffer), "[%03d.%03d.%03d.%03d] %s", a, b, c, d, match[5].str().c_str());
            cout << buffer << endl;
            return 0;
        }
    }
    cout << "INVALID" << endl;
    return 0;
}
EOF

g++ -O3 /app/oracle_normalizer.cpp -o /app/oracle_normalizer
chmod +x /app/oracle_normalizer

useradd -m -s /bin/bash user || true
git init --bare /home/user/netconfig.git

chown -R user:user /home/user/netconfig.git
chmod -R 777 /home/user
chmod -R 777 /app