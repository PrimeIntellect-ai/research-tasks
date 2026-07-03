apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        tesseract-ocr \
        imagemagick \
        golang \
        fonts-dejavu

    pip3 install pytest

    mkdir -p /app
    mkdir -p /opt/oracle

    # Generate the image with the text
    convert -size 400x200 xc:white -font DejaVu-Sans -pointsize 18 -fill black \
    -draw "text 10,50 'TIMEZONE: Pacific/Fiji'" \
    -draw "text 10,100 'SOCKET: /var/run/backend/user.sock'" \
    /app/diagram.png

    # Create the oracle
    cat << 'EOF' > /opt/oracle/user_setup.go
package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	if len(os.Args) < 2 {
		return
	}
	username := strings.ToUpper(os.Args[1])
	fmt.Printf("[Pacific/Fiji] Configuring %s to use /var/run/backend/user.sock\n", username)
}
EOF

    cd /opt/oracle && go build -o user_setup user_setup.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user