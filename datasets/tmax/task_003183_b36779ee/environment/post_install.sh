apt-get update && apt-get install -y \
    python3 python3-pip \
    curl wget espeak \
    protobuf-compiler libprotobuf-dev pkg-config cmake \
    rustc cargo

pip3 install pytest grpcio grpcio-tools SpeechRecognition

mkdir -p /app
espeak -w /app/legacy_equation.wav "ten plus two times open parenthesis five minus one close parenthesis"

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app