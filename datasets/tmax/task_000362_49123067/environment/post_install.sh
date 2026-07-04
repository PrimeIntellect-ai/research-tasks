apt-get update && apt-get install -y python3 python3-pip espeak ffmpeg
pip3 install pytest

mkdir -p /app

cat << 'EOF' > /app/oracle_processor
#!/usr/bin/env python3
import sys

def process():
    raw_data = sys.stdin.buffer.read()

    # 1. Decode cp1252 ignoring errors
    decoded = raw_data.decode('cp1252', errors='ignore')

    # 2. Lowercase normalization
    normalized = decoded.lower()

    # 3. Tokenize by pipe
    tokens = normalized.split('|')

    final_tokens = []
    for t in tokens:
        # 4. Validation gate: drop empty
        if t == '':
            continue
        # 5. Redact tokens containing 'error'
        if 'error' in t:
            final_tokens.append('redacted')
        else:
            final_tokens.append(t)

    # 6. Join with space and encode to UTF-8
    output_str = ' '.join(final_tokens)
    sys.stdout.buffer.write(output_str.encode('utf-8'))

if __name__ == '__main__':
    process()
EOF
chmod +x /app/oracle_processor

espeak -w /app/pipeline_specs.wav "The pipeline expects raw input encoded in cp1252. First, decode the input, ignoring any decoding errors. Next, normalize the text by converting it all to lowercase. Then, tokenize the text by splitting it at every pipe character. For the validation checkpoint, drop any token that is exactly empty. For the remaining tokens, if a token contains the substring 'error', replace the entire token with the word 'redacted'. Finally, join the tokens using a single space, and output the result encoded as UTF-8."

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user