apt-get update && apt-get install -y python3 python3-pip ffmpeg espeak
    pip3 install pytest

    # Install CPU-only torch to save download time and space, then whisper
    pip3 install torch --index-url https://download.pytorch.org/whl/cpu
    pip3 install openai-whisper

    mkdir -p /app

    # Generate the voice memo using espeak
    espeak -w /app/voice_memo.wav "Please build the archive tool to read a tar archive from standard input. Unpack it and recursively traverse the directories. For every file you find, calculate its byte size. If the byte size is strictly greater than fifty bytes, print the file's relative path, followed by a colon, followed by the size in bytes. Ignore empty directories and files that are fifty bytes or smaller. Finally, ensure the printed lines are sorted alphabetically by the file path."

    # Create the oracle program
    cat << 'EOF' > /app/oracle_archive_tool
#!/usr/bin/env python3
import sys
import tarfile

def main():
    try:
        with tarfile.open(fileobj=sys.stdin.buffer, mode='r|*') as tar:
            results = []
            for m in tar:
                if m.isreg() and m.size > 50:
                    results.append(f"{m.name}:{m.size}")
            results.sort()
            for r in results:
                print(r)
    except Exception:
        pass

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/oracle_archive_tool

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user