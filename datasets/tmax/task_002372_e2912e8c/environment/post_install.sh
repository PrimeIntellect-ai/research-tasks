apt-get update && apt-get install -y python3 python3-pip golang openssl socat ffmpeg espeak
    pip3 install pytest

    # Create directories
    mkdir -p /app/bin
    mkdir -p /home/user/iot_configs
    touch /home/user/iot_configs/config1.json
    touch /home/user/iot_configs/config2.json

    for i in 1 2 3 4 5; do
        mkdir -p /home/user/edge_nodes/node_$i
    done

    # Generate audio file
    espeak -w /app/maintenance_recording.wav "The maintenance PIN is 8492"

    # Create reference parser
    cat << 'EOF' > /app/bin/ref_parser.go
package main

import (
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		return
	}
	data, err := base64.StdEncoding.DecodeString(os.Args[1])
	if err != nil {
		return
	}
	for i, j := 0, len(data)-1; i < j; i, j = i+1, j-1 {
		data[i], data[j] = data[j], data[i]
	}
	fmt.Print(hex.EncodeToString(data))
}
EOF
    go build -o /app/bin/ref_parser /app/bin/ref_parser.go
    rm /app/bin/ref_parser.go

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app