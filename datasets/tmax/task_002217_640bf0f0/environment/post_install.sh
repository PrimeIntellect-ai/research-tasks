apt-get update && apt-get install -y python3 python3-pip golang
pip3 install pytest

mkdir -p /app

# Create a dummy transcribe script
cat << 'EOF' > /app/transcribe.sh
#!/bin/bash
echo "Station alpha reports 11.45. Station beta reports 12.80. Station gamma reports 9.50."
EOF
chmod +x /app/transcribe.sh

# Create dummy wav file
touch /app/telemetry.wav

# Create the oracle pipeline in Go
cat << 'EOF' > /app/oracle.go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "math"
    "os"
    "strconv"
    "strings"
)

func round4(val float64) float64 {
    return math.Round(val*10000) / 10000
}

func main() {
    data, _ := io.ReadAll(os.Stdin)
    tokens := strings.Fields(string(data))

    var nums []float64
    for _, t := range tokens {
        if val, err := strconv.ParseFloat(t, 64); err == nil {
            nums = append(nums, val)
        }
    }

    if len(nums) < 2 {
        fmt.Print(`{"error": "insufficient data"}`)
        return
    }

    var sum float64
    for _, n := range nums {
        sum += n
    }
    mean := sum / float64(len(nums))

    var varSum float64
    for _, n := range nums {
        varSum += (n - mean) * (n - mean)
    }
    stddev := math.Sqrt(varSum / float64(len(nums)-1))

    margin := 1.96 * (stddev / math.Sqrt(float64(len(nums))))
    ci_lower := mean - margin
    ci_upper := mean + margin

    class := "NORMAL"
    if ci_lower > 10.0 {
        class = "CRITICAL"
    }

    out := map[string]interface{}{
        "mean":     round4(mean),
        "stddev":   round4(stddev),
        "ci_lower": round4(ci_lower),
        "ci_upper": round4(ci_upper),
        "class":    class,
    }

    b, _ := json.Marshal(out)
    fmt.Print(string(b))
}
EOF

cd /app && go build -o oracle_pipeline oracle.go

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user