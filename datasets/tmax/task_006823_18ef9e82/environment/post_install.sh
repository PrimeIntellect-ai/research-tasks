apt-get update && apt-get install -y python3 python3-pip golang-go
pip3 install pytest

useradd -m -s /bin/bash user || true

cat << 'EOF' > /home/user/server.go
package main

import (
	"encoding/base64"
	"encoding/json"
	"net/http"
	"strings"
)

func evidenceHandler(w http.ResponseWriter, r *http.Request) {
	authHeader := r.Header.Get("Authorization")
	if !strings.HasPrefix(authHeader, "Bearer ") {
		http.Error(w, "Unauthorized: Missing Bearer token", http.StatusUnauthorized)
		return
	}
	token := strings.TrimPrefix(authHeader, "Bearer ")
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		http.Error(w, "Unauthorized: Invalid token format", http.StatusUnauthorized)
		return
	}

	headerJSON, err := base64.RawURLEncoding.DecodeString(parts[0])
	if err != nil {
		http.Error(w, "Unauthorized: Invalid header encoding", http.StatusUnauthorized)
		return
	}
	var header map[string]interface{}
	json.Unmarshal(headerJSON, &header)

	claimsJSON, err := base64.RawURLEncoding.DecodeString(parts[1])
	if err != nil {
		http.Error(w, "Unauthorized: Invalid claims encoding", http.StatusUnauthorized)
		return
	}
	var claims map[string]interface{}
	json.Unmarshal(claimsJSON, &claims)

	alg, _ := header["alg"].(string)
	if strings.ToLower(alg) != "none" {
		if parts[2] != "SUPER_SECRET_SIGNATURE_THAT_YOU_DO_NOT_KNOW" {
			http.Error(w, "Unauthorized: Invalid signature", http.StatusUnauthorized)
			return
		}
	}

	user, _ := claims["user"].(string)
	role, _ := claims["role"].(string)

	if user == "admin" && role == "forensics" {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"target_user": "4261da28713bd7b3554b790dcd017d23", "decoy_user": "098f6bcd4621d373cade4e832627b4f6"}`))
		return
	}

	http.Error(w, "Forbidden: Invalid claims", http.StatusForbidden)
}

func main() {
	http.HandleFunc("/evidence", evidenceHandler)
	http.ListenAndServe("127.0.0.1:8080", nil)
}
EOF

chmod -R 777 /home/user