apt-get update && apt-get install -y python3 python3-pip golang binutils strace
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/suspicious_bin.go
package main

import (
	"fmt"
	"os"
)

func main() {
	if os.Getenv("DROPPER_ENV") != "ACTIVATE" {
		fmt.Println("ERR_ENV_MISSING")
		os.Exit(1)
	}

	if len(os.Args) < 2 {
		fmt.Println("Usage: ./suspicious_bin <key>")
		os.Exit(1)
	}

	key := os.Args[1]

	// Target encoded bytes for "SuperSecretKey123"
	// Formula: encoded[i] = (key[i] ^ 0x2A) + 7
	target := []byte{
		94, 126, 121, 108, 127, 94, 108, 104, 121, 108, 123, 84, 108, 128, 48, 49, 48,
	}

	if len(key) != len(target) {
		fmt.Println("INVALID_KEY_LENGTH")
		os.Exit(1)
	}

	for i := 0; i < len(key); i++ {
		encodedChar := (key[i] ^ 0x2A) + 7
		if encodedChar != target[i] {
			fmt.Println("INVALID_KEY")
			os.Exit(1)
		}
	}

	err := os.WriteFile("/home/user/decrypted_payload.txt", []byte("FLAG{m4lw4r3_r3v3rs3d_succ3ssfullY}"), 0644)
	if err != nil {
		fmt.Println("Error writing payload")
	} else {
		fmt.Println("Payload written to /home/user/decrypted_payload.txt")
	}
}
EOF

    go build -o /home/user/suspicious_bin /tmp/suspicious_bin.go
    rm /tmp/suspicious_bin.go

    cat << 'EOF' > /home/user/keygen.go
package main

import (
	"fmt"
)

// The target encoded bytes extracted from the binary
var targetBytes = []byte{94, 126, 121, 108, 127, 94, 108, 104, 121, 108, 123, 84, 108, 128, 48, 49, 48}

func ReverseTransform(encoded []byte) string {
	decoded := make([]byte, len(encoded))
	for i := 0; i < len(encoded); i++ {
		// BUG: The forward transformation is: encoded[i] = (key[i] ^ 0x2A) + 7
		// The reversal should be: key[i] = (encoded[i] - 7) ^ 0x2A
		// The threat actor wrote the inverse incorrectly:
		decoded[i] = (encoded[i] ^ 0x2A) - 7
	}
	return string(decoded)
}

func main() {
	fmt.Println("Unlock Key:", ReverseTransform(targetBytes))
}
EOF

    chmod -R 777 /home/user