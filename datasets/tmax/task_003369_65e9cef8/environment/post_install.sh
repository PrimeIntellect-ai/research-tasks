apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/upload.go
package main

import (
	"encoding/base64"
	"io/ioutil"
	"net/http"
	"path/filepath"
)

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	encodedFilename := r.URL.Query().Get("filename")
	decoded, err := base64.StdEncoding.DecodeString(encodedFilename)
	if err != nil {
		http.Error(w, "Bad Request", http.StatusBadRequest)
		return
	}

	filename := string(decoded)
	// Vulnerability: Path Traversal (CWE-22)
	destPath := filepath.Join("/var/uploads", filename)

	body, _ := ioutil.ReadAll(r.Body)
	err = ioutil.WriteFile(destPath, body, 0644)
	if err != nil {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
}
EOF

    cat << 'EOF' > /home/user/access.log
192.168.1.5 - - [10/Oct/2023:13:55:36 -0700] "POST /upload?filename=bm9ybWFsX2ZpbGUudHh0 HTTP/1.1" 200 123
192.168.1.6 - - [10/Oct/2023:13:56:00 -0700] "POST /upload?filename=Li4vLi4vLi4vZXRjL3Bhc3N3ZA== HTTP/1.1" 200 456
192.168.1.7 - - [10/Oct/2023:13:57:00 -0700] "POST /upload?filename=Li4vLi4vdmFyL2xvZy9hdXRoLmxvZw== HTTP/1.1" 403 111
192.168.1.8 - - [10/Oct/2023:13:58:00 -0700] "POST /upload?filename=Li4vLi4vLi4vLi4vZXRjL3NoYWRvdw== HTTP/1.1" 200 789
192.168.1.9 - - [10/Oct/2023:13:59:00 -0700] "POST /upload?filename=c2FmZV9waWN0dXJlLnBuZw== HTTP/1.1" 200 234
192.168.1.10 - - [10/Oct/2023:14:00:00 -0700] "POST /upload?filename=Li4vLi4vc2VjcmV0cy50eHQ= HTTP/1.1" 500 56
EOF

    chmod -R 777 /home/user