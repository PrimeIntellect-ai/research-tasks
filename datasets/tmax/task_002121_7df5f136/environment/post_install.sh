apt-get update && apt-get install -y python3 python3-pip golang-go espeak ffmpeg
    pip3 install pytest

    mkdir -p /app

    # Generate the audio file
    espeak -w /app/memo.wav "Set the window size to exactly twenty and impute any missing records with the value negative two point five."

    # Create the oracle pipeline
    cat << 'EOF' > /tmp/oracle.go
package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"math"
	"os"
	"strconv"
)

func main() {
	W := 20
	V := -2.5

	reader := csv.NewReader(os.Stdin)
	var xWindow []float64
	var yWindow []float64

	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil || len(record) < 2 {
			continue
		}

		xVal, errX := strconv.ParseFloat(record[0], 64)
		if errX != nil {
			xVal = V
		}
		yVal, errY := strconv.ParseFloat(record[1], 64)
		if errY != nil {
			yVal = V
		}

		xWindow = append(xWindow, xVal)
		yWindow = append(yWindow, yVal)

		if len(xWindow) > W {
			xWindow = xWindow[1:]
			yWindow = yWindow[1:]
		}

		if len(xWindow) == W {
			var sumX, sumY, sumXY, sumX2, sumY2 float64
			for i := 0; i < W; i++ {
				sumX += xWindow[i]
				sumY += yWindow[i]
				sumXY += xWindow[i] * yWindow[i]
				sumX2 += xWindow[i] * xWindow[i]
				sumY2 += yWindow[i] * yWindow[i]
			}

			wF := float64(W)
			cov := (wF * sumXY) - (sumX * sumY)
			varX := (wF * sumX2) - (sumX * sumX)
			varY := (wF * sumY2) - (sumY * sumY)

			if varX <= 0 || varY <= 0 {
				fmt.Printf("0.0000\n")
			} else {
				corr := cov / math.Sqrt(varX*varY)
				if math.IsNaN(corr) {
					fmt.Printf("0.0000\n")
				} else {
					fmt.Printf("%.4f\n", corr)
				}
			}
		}
	}
}
EOF

    go build -o /app/oracle_pipeline /tmp/oracle.go
    chmod +x /app/oracle_pipeline
    rm /tmp/oracle.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user