apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest

    # Create directories
    mkdir -p /app/vendored/legacyhash
    mkdir -p /opt/oracle

    # Create vendored package
    cat << 'EOF' > /app/vendored/legacyhash/go.mod
module legacyhash

go 1.18
EOF

    cat << 'EOF' > /app/vendored/legacyhash/mixer.go
package legacyhash

func Hash(data []byte) uint64 {
	var v1 uint64 = 0x1234567890abcdef
	for _, b := range data {
		v1 += uint64(b)
		// Rotate left by 13 bits
		v1 = (v1 << 13) | (v1 >> 12)
		v1 ^= 0xdeadbeefcafebabe
	}
	return v1
}
EOF

    # Create and build the oracle
    mkdir -p /tmp/oracle_build
    cd /tmp/oracle_build
    cat << 'EOF' > main.go
package main

import (
	"fmt"
	"os"
)

func Hash(data []byte) uint64 {
	var v1 uint64 = 0x1234567890abcdef
	for _, b := range data {
		v1 += uint64(b)
		// Rotate left by 13 bits
		v1 = (v1 << 13) | (v1 >> 51)
		v1 ^= 0xdeadbeefcafebabe
	}
	return v1
}

func main() {
	if len(os.Args) < 2 {
		return
	}
	fmt.Printf("%016x\n", Hash([]byte(os.Args[1])))
}
EOF
    go mod init oracle
    go build -o /opt/oracle/legacyhash_oracle main.go
    chmod +x /opt/oracle/legacyhash_oracle
    cd /
    rm -rf /tmp/oracle_build

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user