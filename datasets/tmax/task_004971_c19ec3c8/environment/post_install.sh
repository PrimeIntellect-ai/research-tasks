apt-get update && apt-get install -y python3 python3-pip imagemagick fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    convert -size 800x400 xc:white -font DejaVu-Sans -pointsize 16 -fill black -annotate +20+40 "ArtePak RLE Format Specification:\nData is processed in chunks. Every chunk begins with a 1-byte control header.\n- If the Most Significant Bit (MSB) of the header is 1 (header >= 128):\n  The lower 7 bits represent a value N (0 to 127).\n  This indicates a 'Repeat' chunk. You must read exactly ONE following byte of data,\n  and output it (N + 1) times.\n- If the Most Significant Bit (MSB) of the header is 0 (header < 128):\n  The lower 7 bits represent a value N (0 to 127).\n  This indicates a 'Literal' chunk. You must read exactly the next (N + 1) bytes of data\n  from the stream and output them exactly as-is." /app/format_spec.png

    cat << 'EOF' > /app/oracle_decompress
#!/usr/bin/env python3
import sys

def decompress():
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer
    while True:
        header_byte = stdin.read(1)
        if not header_byte:
            break
        header = header_byte[0]
        N = (header & 0x7F) + 1
        if header & 0x80:
            char_to_repeat = stdin.read(1)
            if not char_to_repeat:
                break
            stdout.write(char_to_repeat * N)
        else:
            literal_bytes = stdin.read(N)
            stdout.write(literal_bytes)

if __name__ == "__main__":
    decompress()
EOF

    chmod +x /app/oracle_decompress

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user