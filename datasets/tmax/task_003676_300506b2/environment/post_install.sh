apt-get update && apt-get install -y python3 python3-pip golang-go
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/processor
    cat << 'EOF' > /home/user/processor/go.mod
module processor

go 1.18
EOF

    cat << 'EOF' > /home/user/processor/processor.go
package processor

import "strings"

func ProcessTelemetry(data string) map[string]string {
	result := make(map[string]string)
	if data == "" {
		return result
	}
	fields := strings.Split(data, "|")
	for _, field := range fields {
		kv := strings.Split(field, ":")
		// Bug: panics if kv has length 1
		result[kv[0]] = kv[1]
	}
	return result
}
EOF

    head -c 1024 /dev/urandom > /home/user/dump.bin
    echo -n "ID:8992|TEMP:12.4|STATUS:WARN|CORRUPT_FIELD_NO_COLON" >> /home/user/dump.bin
    head -c 1024 /dev/urandom >> /home/user/dump.bin

    chmod -R 777 /home/user