apt-get update && apt-get install -y python3 python3-pip g++ espeak ffmpeg curl
    pip3 install pytest

    # Install CPU-only torch to save time and space, then whisper
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    pip3 install openai-whisper

    # Pre-download the tiny.en model
    python3 -c "import whisper; whisper.load_model('tiny.en')" || true

    mkdir -p /app

    # Generate the voicemail audio
    espeak -w /app/voicemail.wav "Hey, here are the requirements for the C plus plus text cleaner. The program should read a single line from standard input. First, check if the line starts and ends with a double quote. If it doesn't, or if the line is less than two characters long, just print the word INVALID all caps and exit. If it is valid, strip the surrounding double quotes. Next, find all unicode escape sequences in the format backslash, lowercase u, followed by exactly four hex digits. Decode these specific sequences into their corresponding UTF-8 characters. Leave any invalid or unrecognized escape sequences exactly as they are. Then, use a regular expression to extract all words consisting entirely of one or more English alphabet letters, either uppercase or lowercase. Now, iterate through these extracted words using a sliding window of exactly three consecutive words. For each three-word window, compute a hash by concatenating the three words with a single space between them, and summing the ASCII integer values of all characters in that concatenated string. Finally, deduplicate these window hashes. Print the final string length of the decoded text, a comma, a space, and the count of unique window hashes. For example, Length: 45, Unique Windows: 2"

    # Create oracle cleaner C++ source
    cat << 'EOF' > /app/oracle_cleaner.cpp
#include <iostream>
#include <string>
#include <regex>
#include <vector>
#include <unordered_set>

using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;

    if (line.length() < 2 || line.front() != '"' || line.back() != '"') {
        cout << "INVALID\n";
        return 0;
    }

    string stripped = line.substr(1, line.length() - 2);

    string decoded;
    for (size_t i = 0; i < stripped.length(); ) {
        if (i + 5 < stripped.length() && stripped[i] == '\\' && stripped[i+1] == 'u') {
            bool hex = true;
            for (int j = 0; j < 4; ++j) {
                if (!isxdigit(stripped[i+2+j])) { hex = false; break; }
            }
            if (hex) {
                int code = stoi(stripped.substr(i+2, 4), nullptr, 16);
                if (code <= 0x7F) {
                    decoded += (char)code;
                } else if (code <= 0x7FF) {
                    decoded += (char)(0xC0 | ((code >> 6) & 0x1F));
                    decoded += (char)(0x80 | (code & 0x3F));
                } else {
                    decoded += (char)(0xE0 | ((code >> 12) & 0x0F));
                    decoded += (char)(0x80 | ((code >> 6) & 0x3F));
                    decoded += (char)(0x80 | (code & 0x3F));
                }
                i += 6;
                continue;
            }
        }
        decoded += stripped[i];
        i++;
    }

    regex word_regex("[a-zA-Z]+");
    auto words_begin = sregex_iterator(decoded.begin(), decoded.end(), word_regex);
    auto words_end = sregex_iterator();

    vector<string> words;
    for (sregex_iterator i = words_begin; i != words_end; ++i) {
        words.push_back(i->str());
    }

    unordered_set<int> hashes;
    if (words.size() >= 3) {
        for (size_t i = 0; i <= words.size() - 3; ++i) {
            string window = words[i] + " " + words[i+1] + " " + words[i+2];
            int hash = 0;
            for (char c : window) hash += (unsigned char)c;
            hashes.insert(hash);
        }
    }

    cout << "Length: " << decoded.length() << ", Unique Windows: " << hashes.size() << "\n";
    return 0;
}
EOF

    # Compile the oracle cleaner
    g++ -O3 -std=c++17 /app/oracle_cleaner.cpp -o /app/oracle_cleaner
    chmod +x /app/oracle_cleaner

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user