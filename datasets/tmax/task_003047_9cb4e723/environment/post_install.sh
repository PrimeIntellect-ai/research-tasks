apt-get update && apt-get install -y python3 python3-pip g++ make valgrind
    pip3 install pytest

    mkdir -p /app/cpp-base64
    mkdir -p /home/user/crash
    mkdir -p /opt/oracle

    # Create base64.h
    cat << 'EOF' > /app/cpp-base64/base64.h
#ifndef BASE64_H
#define BASE64_H
#include <string>
std::string base64_decode(std::string const& s);
#endif
EOF

    # Create correct base64.cpp for the oracle
    cat << 'EOF' > /app/cpp-base64/base64_correct.cpp
#include "base64.h"
#include <vector>
static const std::string base64_chars = 
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789+/";
static inline bool is_base64(unsigned char c) {
  return (isalnum(c) || (c == '+') || (c == '/'));
}
std::string base64_decode(std::string const& encoded_string) {
  int in_len = encoded_string.size();
  int i = 0, j = 0, in_ = 0;
  unsigned char char_array_4[4], char_array_3[3];
  std::string ret;
  while (in_len-- && ( encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
    char_array_4[i++] = encoded_string[in_]; in_++;
    if (i == 4) {
      for (i = 0; i < 4; i++)
        char_array_4[i] = base64_chars.find(char_array_4[i]);
      char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
      char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
      char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];
      for (i = 0; (i < 3); i++) ret += char_array_3[i];
      i = 0;
    }
  }
  if (i) {
    for (j = i; j < 4; j++) char_array_4[j] = 0;
    for (j = 0; j < 4; j++) char_array_4[j] = base64_chars.find(char_array_4[j]);
    char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
    char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
    char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];
    for (j = 0; (j < i - 1); j++) ret += char_array_3[j];
  }
  return ret;
}
EOF

    # Create buggy base64.cpp for the agent
    sed 's/while (in_len-- &&/while (in_len \&\&/' /app/cpp-base64/base64_correct.cpp > /app/cpp-base64/base64.cpp

    # Create correct service_worker.cpp for the oracle
    cat << 'EOF' > /app/service_worker_correct.cpp
#include <iostream>
#include <string>
#include "cpp-base64/base64.h"

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        try {
            std::string decoded = base64_decode(line);
            char* output_buffer = new char[decoded.size() + 1];
            std::copy(decoded.begin(), decoded.end(), output_buffer);
            output_buffer[decoded.size()] = '\0';

            bool success = true;
            for (char c : line) {
                if (c == '!' || c == '@' || c == '\xff') {
                    success = false;
                    break;
                }
            }

            if (!success) {
                delete[] output_buffer;
                continue;
            }

            std::cout << output_buffer << std::endl;
            delete[] output_buffer;
        } catch (...) {
            continue;
        }
    }
    return 0;
}
EOF

    # Create buggy service_worker.cpp for the agent
    sed '/delete\[\] output_buffer;/d' /app/service_worker_correct.cpp > /app/service_worker.cpp
    # Re-add the correct delete[] at the very end of the success path
    sed -i 's/std::cout << output_buffer << std::endl;/std::cout << output_buffer << std::endl;\n            delete[] output_buffer;/g' /app/service_worker.cpp

    # Compile the oracle
    g++ -O3 /app/service_worker_correct.cpp /app/cpp-base64/base64_correct.cpp -o /opt/oracle/worker_oracle
    strip /opt/oracle/worker_oracle

    # Create Makefile
    cat << 'EOF' > /app/Makefile
all:
	g++ -g -O0 service_worker.cpp cpp-base64/base64.cpp -o worker
EOF

    # Create dummy crash files
    touch /home/user/crash/core
    echo "Processing input... CRASH" > /home/user/crash/service.log

    # Cleanup correct files so agent doesn't see them
    rm /app/cpp-base64/base64_correct.cpp /app/service_worker_correct.cpp

    useradd -m -s /bin/bash user || true
    chown -R user:user /app /home/user /opt/oracle
    chmod -R 777 /home/user