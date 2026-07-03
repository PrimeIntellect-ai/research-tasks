apt-get update && apt-get install -y python3 python3-pip wget git
    pip3 install pytest

    # Install Go 1.21
    wget -q https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
    rm go1.21.6.linux-amd64.tar.gz
    export PATH=/usr/local/go/bin:$PATH

    # Build the oracle decoder
    mkdir -p /tmp/oracle_build
    cd /tmp/oracle_build
    cat << 'EOF' > main.go
package main

import (
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/Luzifer/go-openssl"
)

func main() {
	input, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		os.Exit(1)
	}

	decoded, err := base64.StdEncoding.DecodeString(string(input))
	if err != nil {
		os.Exit(1)
	}

	o := openssl.New()
	decrypted, err := o.DecryptBytes("CSP_Secret_Key_2024", decoded)
	if err != nil {
		os.Exit(1)
	}

	fmt.Print(string(decrypted))
}
EOF
    go mod init oracle
    go get github.com/Luzifer/go-openssl@v2.0.0
    mkdir -p /opt/oracle
    go build -ldflags="-s -w" -o /opt/oracle/decoder main.go
    chmod +x /opt/oracle/decoder
    cd /
    rm -rf /tmp/oracle_build

    # Setup the vendored package with perturbation
    mkdir -p /app/vendor/github.com/Luzifer
    cd /app/vendor/github.com/Luzifer
    git clone https://github.com/Luzifer/go-openssl.git
    cd go-openssl
    git checkout v2.0.0
    sed -i 's/Salted__/Hacked__/g' openssl.go
    chmod -R 777 /app/vendor

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user