apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest

    cat << 'EOF' > /tmp/oracle.go
package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func main() {
	bytes, err := io.ReadAll(os.Stdin)
	if err != nil {
		return
	}
	fields := strings.Fields(string(bytes))
	if len(fields) < 2 {
		fmt.Println("0.000000")
		return
	}

	var rates []float64
	for _, f := range fields {
		v, _ := strconv.ParseFloat(f, 64)
		rates = append(rates, v)
	}

	sum := 0.0
	dt := 1.0
	for i := 0; i < len(rates)-1; i++ {
		sum += (rates[i] + rates[i+1]) / 2.0 * dt
		dt *= 1.5
	}
	fmt.Printf("%.6f\n", sum)
}
EOF

    mkdir -p /app
    go build -ldflags="-s -w" -o /app/divergence_scorer /tmp/oracle.go
    chmod +x /app/divergence_scorer
    rm /tmp/oracle.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user