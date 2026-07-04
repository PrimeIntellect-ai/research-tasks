apt-get update && apt-get install -y python3 python3-pip golang-go
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user
    cd /home/user

    cat << 'EOF' > /home/user/upload.log
10.0.0.1 - GET /index.html 200 -
192.168.1.100 - POST /upload?path=../../../etc/passwd 403 AKIAIOSFODNN7EXAMPLE
172.16.0.5 - POST /upload?path=images/logo.png 200 AKIATEST1234567890AB
10.0.0.2 - GET /static/app.js 200 -
192.168.1.101 - GET /download?file=../config.json 200 -
192.168.1.100 - POST /upload?path=../uploads/shell.php 200 AKIABADGUY9999999999
EOF

    cat << 'EOF' > /home/user/upload_clean_expected.log
10.0.0.1 - GET /index.html 200 -
192.168.1.100 - POST /upload?path=../../../etc/passwd 403 [REDACTED]
172.16.0.5 - POST /upload?path=images/logo.png 200 [REDACTED]
10.0.0.2 - GET /static/app.js 200 -
192.168.1.101 - GET /download?file=../config.json 200 -
192.168.1.100 - POST /upload?path=../uploads/shell.php 200 [REDACTED]
EOF

    cat << 'EOF' > /home/user/setup.go
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"crypto/sha256"
	"log"
	"os"
)

func main() {
	cleanLog, err := os.ReadFile("/home/user/upload_clean_expected.log")
	if err != nil {
		log.Fatal(err)
	}

	hash := sha256.Sum256(cleanLog)

	plaintext := []byte("SUPER_SECRET_ROTATED_CREDENTIALS_99283")

	block, err := aes.NewCipher(hash[:])
	if err != nil {
		log.Fatal(err)
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		log.Fatal(err)
	}

	nonce := make([]byte, 12)
	if _, err := rand.Read(nonce); err != nil {
		log.Fatal(err)
	}

	ciphertext := aesgcm.Seal(nil, nonce, plaintext, nil)

	finalData := append(nonce, ciphertext...)
	os.WriteFile("/home/user/new_creds.aes", finalData, 0644)
}
EOF

    go run /home/user/setup.go
    rm /home/user/setup.go /home/user/upload_clean_expected.log

    chown -R user:user /home/user
    chmod -R 777 /home/user