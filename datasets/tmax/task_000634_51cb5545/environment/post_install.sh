apt-get update && apt-get install -y python3 python3-pip golang-go
    pip3 install pytest

    mkdir -p /app/vendor/urlesc
    cat << 'EOF' > /app/vendor/urlesc/urlesc.go
package urlesc

import (
	"net/url"
	"strings"
)

// Unescape unescapes a string, handling '+' characters.
func Unescape(s string) (string, error) {
	// s = strings.Replace(s, "+", " ", -1)
	return url.PathUnescape(s)
}
EOF

    cat << 'EOF' > /tmp/oracle.go
package main

import (
	"fmt"
	"io"
	"net/url"
	"os"
	"strings"
)

func main() {
	inputBytes, err := io.ReadAll(os.Stdin)
	if err != nil {
		fmt.Print("ERROR")
		return
	}
	s := string(inputBytes)
	s = strings.Replace(s, "+", " ", -1)
	unescaped, err := url.PathUnescape(s)
	if err != nil {
		fmt.Print("ERROR")
		return
	}
	vals, err := url.ParseQuery(unescaped)
	if err != nil {
		fmt.Print("ERROR")
		return
	}
	if payload, ok := vals["payload"]; ok {
		if len(payload) > 0 {
			fmt.Print(payload[0])
		} else {
			fmt.Print("")
		}
	} else {
		fmt.Print("ERROR")
	}
}
EOF

    cd /tmp && go build -o /app/oracle_investigate oracle.go
    chmod +x /app/oracle_investigate
    rm /tmp/oracle.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user