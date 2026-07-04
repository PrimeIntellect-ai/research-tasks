apt-get update && apt-get install -y python3 python3-pip curl openssl golang-go
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/main.go
package main

import (
	"encoding/base64"
	"fmt"
	"net/http"
	"os"
	"strings"
)

func main() {
	var cert, key, port string
	for i := 1; i < len(os.Args); i++ {
		if os.Args[i] == "--cert" && i+1 < len(os.Args) {
			cert = os.Args[i+1]
		} else if os.Args[i] == "--key" && i+1 < len(os.Args) {
			key = os.Args[i+1]
		} else if os.Args[i] == "--port" && i+1 < len(os.Args) {
			port = os.Args[i+1]
		}
	}

	if cert == "" || key == "" || port == "" {
		os.Exit(1)
	}

	http.HandleFunc("/api/v1/evidence", func(w http.ResponseWriter, r *http.Request) {
		auth := r.Header.Get("Authorization")
		if !strings.HasPrefix(auth, "Bearer ") {
			http.Error(w, "Unauthorized", 401)
			return
		}
		token := strings.TrimPrefix(auth, "Bearer ")
		parts := strings.Split(token, ".")
		if len(parts) < 2 {
			http.Error(w, "Unauthorized", 401)
			return
		}

		headerBytes, _ := base64.RawURLEncoding.DecodeString(parts[0])
		payloadBytes, _ := base64.RawURLEncoding.DecodeString(parts[1])

		headerStr := strings.ReplaceAll(string(headerBytes), " ", "")
		payloadStr := string(payloadBytes)

		if strings.Contains(headerStr, `"alg":"none"`) && strings.Contains(payloadStr, `"access_level":"system"`) {
			chunk := r.URL.Query().Get("chunk")
			fmt.Fprintf(w, "EVIDENCE_CHUNK_%s_abcdef123456\n", chunk)
			return
		}
		http.Error(w, "Unauthorized", 401)
	})

	http.ListenAndServeTLS("0.0.0.0:"+port, cert, key, nil)
}
EOF

    cd /app
    go build -ldflags="-s -w" -o vault_server main.go
    rm main.go
    apt-get remove -y golang-go
    apt-get autoremove -y

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user