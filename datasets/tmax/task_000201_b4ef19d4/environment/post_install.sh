apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest Pillow

    mkdir -p /app
    mkdir -p /opt/verifier

    # Create the format schematic image
    cat << 'EOF' > /tmp/make_image.py
from PIL import Image, ImageDraw
img = Image.new('RGB', (800, 200), color = (255, 255, 255))
d = ImageDraw.Draw(img)
text = """Custom Hex RLE Format v2:
1. Standard bytes are represented as 2-character hex codes (e.g., A5, 00, FF).
2. RLE compression is denoted by a colon followed by a decimal multiplier (e.g., FF:4 means FFFFFFFF).
3. Max multiplier is 255. Multipliers > 255 or < 1 are INVALID.
4. Odd-length hex sequences before a colon or EOF are INVALID.
5. Non-hex characters (except colon and digits following it) are INVALID."""
d.text((10,10), text, fill=(0,0,0))
img.save('/app/format_schematic.png')
EOF
    python3 /tmp/make_image.py

    # Create the oracle decoder C++ source
    cat << 'EOF' > /tmp/oracle.cpp
#include <iostream>
#include <string>
#include <cctype>
#include <cstdlib>

using namespace std;

void fail() {
    cout << "INVALID\n";
    exit(1);
}

int main(int argc, char** argv) {
    if (argc != 2) fail();
    string s = argv[1];
    string out = "";
    int i = 0;
    while(i < s.length()) {
        string hex = "";
        while(i < s.length() && s[i] != ':') {
            if(!isxdigit(s[i])) fail();
            hex += s[i];
            i++;
        }
        if(hex.length() % 2 != 0) fail();
        int mult = 1;
        if(i < s.length() && s[i] == ':') {
            i++;
            string m = "";
            while(i < s.length() && isdigit(s[i])) {
                m += s[i];
                i++;
            }
            if(m == "") fail();
            mult = stoi(m);
            if(mult < 1 || mult > 255) fail();
        }
        for(int k=0; k<mult; k++) out += hex;
    }
    cout << out << "\n";
    return 0;
}
EOF
    g++ -O3 /tmp/oracle.cpp -o /opt/verifier/oracle_decoder
    cp /opt/verifier/oracle_decoder /app/legacy_decoder

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user