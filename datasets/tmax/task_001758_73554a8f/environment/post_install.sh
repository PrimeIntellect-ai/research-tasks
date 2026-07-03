apt-get update && apt-get install -y python3 python3-pip espeak
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user

    # Generate the voicemail.wav using espeak
    espeak -w /app/voicemail.wav "Hey, it's Sarah. The retry bug is causing dirty duplicates. To clean the dataset, your script must process each line as follows: First, strip all leading and trailing whitespace. Second, replace any sequence of multiple spaces with a single space. Third, remove all characters that are not alphanumeric and not a space. Fourth, convert all characters to uppercase. After applying this to every line, remove any duplicate lines. Finally, output the unique lines sorted in descending alphabetical order."

    # Create the oracle filter
    cat << 'EOF' > /app/oracle_filter
#!/usr/bin/env python3
import sys
import re

def process():
    unique_lines = set()
    for line in sys.stdin:
        # 1. Strip leading/trailing whitespace
        s = line.strip()
        # 2. Replace multiple spaces with a single space
        s = re.sub(r' +', ' ', s)
        # 3. Remove non-alphanumeric except spaces
        s = re.sub(r'[^a-zA-Z0-9 ]', '', s)
        # 4. Convert to uppercase
        s = s.upper()
        unique_lines.add(s)

    # 5 & 6. Sort in descending alphabetical order and output
    for out_line in sorted(list(unique_lines), reverse=True):
        print(out_line)

if __name__ == '__main__':
    process()
EOF
    chmod +x /app/oracle_filter

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user