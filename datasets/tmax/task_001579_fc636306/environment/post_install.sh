apt-get update && apt-get install -y python3 python3-pip espeak ffmpeg gcc
    pip3 install pytest

    mkdir -p /app
    espeak -w /app/compliance_dictation.wav "Write a C program that reads space-separated lines from standard input. Each line has three integers: User ID, Transaction ID, and Amount. The data arrives ordered sequentially by Transaction ID. For each User ID, calculate the running total of the Amount. Output each line as User ID, Transaction ID, and the running total. If the running total is strictly greater than five thousand, append a one, otherwise append a zero. Separate all output values with a single space and end each line with a newline."

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user