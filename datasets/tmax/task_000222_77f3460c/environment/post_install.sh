apt-get update && apt-get install -y python3 python3-pip golang-go espeak
    pip3 install pytest

    mkdir -p /app

    # Generate the audio memo
    espeak -w /app/memo.wav "The affected subnet is 1 7 2 dot 1 6 dot 0 dot 0 slash 12. The emergency backup recovery key is alpha-tango-niner."

    # Create the oracle program
    cat << 'EOF' > /app/oracle.go
package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
	_, subnet, _ := net.ParseCIDR("172.16.0.0/12")
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, ",")
		if len(parts) != 3 {
			continue
		}
		deviceID := parts[0]
		ipStr := parts[1]
		status := parts[2]

		ip := net.ParseIP(ipStr)
		if status == "OFFLINE" && ip != nil && subnet.Contains(ip) {
			fmt.Printf("%s RECOVER alpha-tango-niner\n", deviceID)
		} else {
			fmt.Printf("%s IGNORE\n", deviceID)
		}
	}
}
EOF

    go build -o /app/oracle_telemetry_filter /app/oracle.go
    chmod +x /app/oracle_telemetry_filter

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user