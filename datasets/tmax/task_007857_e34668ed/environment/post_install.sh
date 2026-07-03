apt-get update && apt-get install -y python3 python3-pip golang curl
pip3 install pytest

mkdir -p /home/user/vuln
mkdir -p /home/user/redteam

cat << 'EOF' > /home/user/vuln/main.go
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/tls"
	"encoding/hex"
	"io"
	"net/http"
	"os/exec"
)

func runRemoteHandler(w http.ResponseWriter, r *http.Request) {
	targetURL := r.URL.Query().Get("url")
	keyHex := r.URL.Query().Get("key")

	if targetURL == "" || keyHex == "" {
		http.Error(w, "missing url or key", http.StatusBadRequest)
		return
	}

	key, err := hex.DecodeString(keyHex)
	if err != nil || len(key) != 32 {
		http.Error(w, "invalid key", http.StatusBadRequest)
		return
	}

	// CWE-295: Improper Certificate Validation
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{Transport: tr}

	resp, err := client.Get(targetURL)
	if err != nil {
		http.Error(w, "fetch failed", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	data, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "read failed", http.StatusInternalServerError)
		return
	}

	if len(data) < 12 {
		http.Error(w, "data too short", http.StatusBadRequest)
		return
	}

	nonce := data[:12]
	ciphertext := data[12:]

	block, err := aes.NewCipher(key)
	if err != nil {
		http.Error(w, "cipher error", http.StatusInternalServerError)
		return
	}

	aesgcm, err := cipher.NewGCM(block)
	if err != nil {
		http.Error(w, "gcm error", http.StatusInternalServerError)
		return
	}

	plaintext, err := aesgcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		http.Error(w, "decrypt error", http.StatusInternalServerError)
		return
	}

	// CWE-78: Improper Neutralization of Special Elements used in an OS Command
	cmd := exec.Command("sh", "-c", string(plaintext))
	err = cmd.Run()
	if err != nil {
		http.Error(w, "exec failed", http.StatusInternalServerError)
		return
	}

	w.Write([]byte("Success"))
}

func main() {
	http.HandleFunc("/run_remote", runRemoteHandler)
	http.ListenAndServe("127.0.0.1:8080", nil)
}
EOF

# Build the vulnerable server
cd /home/user/vuln
go build -o vuln_server main.go

# Add user
useradd -m -s /bin/bash user || true

# Make a script to run the server in the background when bash starts
echo "cd /home/user/vuln && ./vuln_server &" >> /home/user/.bashrc
echo "sleep 1" >> /home/user/.bashrc

chmod -R 777 /home/user