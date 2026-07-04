apt-get update && apt-get install -y python3 python3-pip g++ openssl libssl-dev
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/audit_target
    cd /home/user/audit_target

    cat << 'EOF' > auth_cli.cpp
#include <iostream>
#include <string>
#include <vector>

std::string decode_base64url(const std::string& input) {
    std::string out;
    std::string b64 = input;
    for (char& c : b64) {
        if (c == '-') c = '+';
        else if (c == '_') c = '/';
    }
    return b64; 
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " --verify <token>\n";
        return 1;
    }

    std::string action = argv[1];
    std::string token = argv[2];

    if (action != "--verify") { return 1; }

    size_t first_dot = token.find('.');
    size_t second_dot = token.find('.', first_dot + 1);

    if (first_dot == std::string::npos || second_dot == std::string::npos) {
        std::cerr << "Invalid token format.\n";
        return 1;
    }

    std::string header = token.substr(0, first_dot);
    std::string payload = token.substr(first_dot + 1, second_dot - first_dot - 1);
    std::string signature = token.substr(second_dot + 1);

    std::string cmd = "python3 -c \"import sys, json, base64;"
                      "h=json.loads(base64.urlsafe_b64decode(sys.argv[1] + '===').decode());"
                      "p=json.loads(base64.urlsafe_b64decode(sys.argv[2] + '===').decode());"
                      "sys.exit(0 if h.get('alg').lower() == 'none' and p.get('user') == 'sysadmin_992' and p.get('role') == 'admin' else 1)\" " 
                      + header + " " + payload + " >/dev/null 2>&1";

    int res = system(cmd.c_str());
    if (res == 0) {
        std::cout << "FLAG{alg_none_priv_esc_successful}" << std::endl;
        return 0;
    } else {
        std::cerr << "Signature validation failed or invalid payload.\n";
        return 1;
    }
}
EOF

    g++ -O2 auth_cli.cpp -o auth_cli

    echo "admin_username=sysadmin_992" > users.db
    openssl enc -aes-256-cbc -pbkdf2 -salt -in users.db -out users.db.enc -pass pass:482
    rm users.db

    chown -R user:user /home/user/audit_target
    chmod -R 777 /home/user