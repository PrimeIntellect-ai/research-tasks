apt-get update && apt-get install -y python3 python3-pip golang ffmpeg
    pip3 install pytest

    mkdir -p /app

    # Create the Go oracle
    cat << 'EOF' > /app/oracle.go
package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"sort"
)

type Record struct {
	ScreenID    int    `json:"screen_id"`
	Key         string `json:"key"`
	Translation string `json:"translation"`
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var records []Record
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			continue
		}
		var r Record
		if err := json.Unmarshal([]byte(line), &r); err == nil {
			records = append(records, r)
		}
	}

	grouped := make(map[int][]Record)
	for _, r := range records {
		grouped[r.ScreenID] = append(grouped[r.ScreenID], r)
	}

	times := []string{
		"00:00:00,000 --> 00:00:01,500",
		"00:00:01,500 --> 00:00:04,000",
		"00:00:04,000 --> 00:00:05,250",
		"00:00:05,250 --> 00:00:08,000",
		"00:00:08,000 --> 00:00:10,000",
	}

	for i := 1; i <= 5; i++ {
		fmt.Printf("%d\n%s\nScreen %d:\n", i, times[i-1], i)
		recs := grouped[i]
		if len(recs) == 0 {
			fmt.Printf("- DEFAULT: Missing\n")
		} else {
			sort.Slice(recs, func(a, b int) bool {
				return recs[a].Key < recs[b].Key
			})
			for _, r := range recs {
				fmt.Printf("- %s: %s\n", r.Key, r.Translation)
			}
		}
		fmt.Printf("\n")
	}
}
EOF

    cd /app
    go build -o oracle_render oracle.go
    chmod +x oracle_render

    # Generate the reference video
    ffmpeg -f lavfi -i color=c=red:s=320x240:d=1.5 -c:v libx264 -pix_fmt yuv420p /tmp/c1.mp4
    ffmpeg -f lavfi -i color=c=green:s=320x240:d=2.5 -c:v libx264 -pix_fmt yuv420p /tmp/c2.mp4
    ffmpeg -f lavfi -i color=c=blue:s=320x240:d=1.25 -c:v libx264 -pix_fmt yuv420p /tmp/c3.mp4
    ffmpeg -f lavfi -i color=c=yellow:s=320x240:d=2.75 -c:v libx264 -pix_fmt yuv420p /tmp/c4.mp4
    ffmpeg -f lavfi -i color=c=cyan:s=320x240:d=2.0 -c:v libx264 -pix_fmt yuv420p /tmp/c5.mp4

    cat <<EOF > /tmp/inputs.txt
file '/tmp/c1.mp4'
file '/tmp/c2.mp4'
file '/tmp/c3.mp4'
file '/tmp/c4.mp4'
file '/tmp/c5.mp4'
EOF

    ffmpeg -f concat -safe 0 -i /tmp/inputs.txt -c copy /app/loc_reference.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user