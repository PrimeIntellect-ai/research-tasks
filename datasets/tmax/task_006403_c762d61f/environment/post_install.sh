apt-get update && apt-get install -y python3 python3-pip golang-go procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/service_src
    cd /home/user/service_src

    cat << 'EOF' > main.go
package main

import (
	"encoding/base64"
	"encoding/json"
	"net/http"
	"strings"
)

func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		authHeader := r.Header.Get("Authorization")
		if !strings.HasPrefix(authHeader, "Bearer ") {
			http.Error(w, "Missing or invalid token", http.StatusUnauthorized)
			return
		}
		token := strings.TrimPrefix(authHeader, "Bearer ")
		parts := strings.Split(token, ".")
		if len(parts) != 3 {
			http.Error(w, "Malformed token", http.StatusUnauthorized)
			return
		}

		headerDec, err := base64.RawURLEncoding.DecodeString(parts[0])
		if err != nil {
			http.Error(w, "Invalid header", http.StatusUnauthorized)
			return
		}

		var header map[string]interface{}
		json.Unmarshal(headerDec, &header)

		payloadDec, err := base64.RawURLEncoding.DecodeString(parts[1])
		if err != nil {
			http.Error(w, "Invalid payload", http.StatusUnauthorized)
			return
		}

		var payload map[string]interface{}
		json.Unmarshal(payloadDec, &payload)

		// Vulnerability: If alg is none, skip signature check
		alg, _ := header["alg"].(string)
		if strings.ToLower(alg) != "none" {
			// Fake signature validation failure for anything else
			http.Error(w, "Invalid signature", http.StatusUnauthorized)
			return
		}

		role, _ := payload["role"].(string)
		if role != "admin" {
			http.Error(w, "Forbidden: Admins only", http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)
	}
}

func rotateHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(`{"status":"success","new_key":"SECRET_KEY_998877_ROTATED"}`))
}

func main() {
	// Obfuscated endpoint name to require binary analysis
	http.HandleFunc("/api/v2/admin/system_rotate_credentials_x912", authMiddleware(rotateHandler))
	http.ListenAndServe("127.0.0.1:8080", nil)
}
EOF

    go mod init legacy
    go build -o /home/user/legacy_service main.go
    cd /
    rm -rf /home/user/service_src

    # Ensure the service starts automatically when the user logs in or tests run
    cat << 'EOF' >> /home/user/.bashrc
if ! pgrep -x "legacy_service" > /dev/null
then
    /home/user/legacy_service &
    sleep 1
fi
EOF

    # Also start it for root in case tests run as root
    cat << 'EOF' >> /root/.bashrc
if ! pgrep -x "legacy_service" > /dev/null
then
    /home/user/legacy_service &
    sleep 1
fi
EOF

    chmod -R 777 /home/user