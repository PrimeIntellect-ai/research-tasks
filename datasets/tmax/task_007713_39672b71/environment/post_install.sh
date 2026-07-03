apt-get update && apt-get install -y python3 python3-pip golang-go openssl
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/server/certs
    cd /home/user/server/certs

    # Generate CA and server certs
    openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -days 365 -nodes -subj "/C=US/ST=CA/L=SanFrancisco/O=Pentest Corp/CN=Vulnerable Pentest CA"
    openssl req -newkey rsa:2048 -keyout server.key -out server.csr -nodes -subj "/C=US/ST=CA/L=SanFrancisco/O=Pentest Corp/CN=localhost"
    openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

    cd /home/user/server
    cat << 'EOF' > main.go
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
	"strings"
)

var secretKey = make([]byte, 16)

func init() {
	rand.Read(secretKey)
}

func encrypt(plaintext []byte) string {
	block, _ := aes.NewCipher(secretKey)
	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	iv := ciphertext[:aes.BlockSize]
	io.ReadFull(rand.Reader, iv)

	stream := cipher.NewCTR(block, iv)
	stream.XORKeyStream(ciphertext[aes.BlockSize:], plaintext)

	return base64.StdEncoding.EncodeToString(ciphertext)
}

func decrypt(cryptoText string) string {
	ciphertext, _ := base64.StdEncoding.DecodeString(cryptoText)
	block, _ := aes.NewCipher(secretKey)

	if len(ciphertext) < aes.BlockSize {
		return ""
	}
	iv := ciphertext[:aes.BlockSize]
	ciphertext = ciphertext[aes.BlockSize:]

	stream := cipher.NewCTR(block, iv)
	stream.XORKeyStream(ciphertext, ciphertext)

	return string(ciphertext)
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	username := r.URL.Query().Get("username")
	if username == "" {
		username = "anonymous"
	}

	// Create cookie
	cookieVal := fmt.Sprintf("username=%s", username)
	enc := encrypt([]byte(cookieVal))

	http.SetCookie(w, &http.Cookie{
		Name:  "auth_token",
		Value: enc,
	})

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Logged in as " + username))
}

func adminHandler(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("auth_token")
	if err != nil {
		http.Error(w, "Missing cookie", http.StatusUnauthorized)
		return
	}

	dec := decrypt(cookie.Value)
	if strings.Contains(dec, "username=admin") {
		w.Write([]byte("FLAG{b1t_fl1pp1ng_m4st3r_992}"))
	} else {
		http.Error(w, "Access denied. You are: "+dec, http.StatusForbidden)
	}
}

func main() {
	http.HandleFunc("/login", loginHandler)
	http.HandleFunc("/admin", adminHandler)

	err := http.ListenAndServeTLS("127.0.0.1:8443", "certs/server.crt", "certs/server.key", nil)
	if err != nil {
		panic(err)
	}
}
EOF

    chown -R user:user /home/user/server
    chmod -R 777 /home/user