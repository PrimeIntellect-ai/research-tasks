apt-get update && apt-get install -y python3 python3-pip golang ffmpeg imagemagick gawk
    pip3 install pytest

    mkdir -p /home/user/video_pipeline
    mkdir -p /app

    # Create dummy video
    ffmpeg -f lavfi -i testsrc=duration=2:size=320x240:rate=5 -c:v libx264 -pix_fmt yuv420p /app/incident_recording.mp4

    # Create reference metrics
    ffmpeg -i /app/incident_recording.mp4 -vf "format=gray,signalstats" -f null - 2>&1 | grep "Parsed_signalstats" | awk -F'YAVG:' '{print $2}' | awk '{print $1}' > /tmp/yavg.txt
    python3 -c "
import json
with open('/tmp/yavg.txt') as f:
    lines = f.read().splitlines()
data = [{'frame': i, 'brightness': float(v)} for i, v in enumerate(lines)]
with open('/tmp/reference_metrics.json', 'w') as f:
    json.dump(data, f)
"

    # Create extract_frames.sh
    cat << 'EOF' > /home/user/video_pipeline/extract_frames.sh
#!/bin/bash
# Bug: no quotes around $1
ffmpeg -i $1 -vf fps=5 /tmp/frames_%04d.png
EOF
    chmod +x /home/user/video_pipeline/extract_frames.sh

    # Create main.go
    cat << 'EOF' > /home/user/video_pipeline/main.go
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"sync"
)

type Metric struct {
	Frame      int     `json:"frame"`
	Brightness float64 `json:"brightness"`
}

func main() {
	input := flag.String("input", "", "input video")
	output := flag.String("output", "", "output json")
	flag.Parse()

	if *input == "" || *output == "" {
		return
	}

	// Broken async attempt
	var wg sync.WaitGroup
	metrics := make(map[int]float64)

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(frame int) {
			defer wg.Done()
			// Data race
			metrics[frame] = math.NaN()
		}(i)
	}
	wg.Wait()

	var result []Metric
	for k, v := range metrics {
		result = append(result, Metric{Frame: k, Brightness: v})
	}

	// Unsafe JSON marshaling (NaN will panic or fail)
	data, err := json.Marshal(result)
	if err != nil {
		fmt.Println("Error:", err)
	}
	ioutil.WriteFile(*output, data, 0644)
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user