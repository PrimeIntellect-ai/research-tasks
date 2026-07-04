apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Install required system packages
    apt-get install -y ffmpeg tesseract-ocr fonts-dejavu-core golang-go

    # Create directories
    mkdir -p /app/data /app/bin /home/user

    # Generate the reference video
    for id in 10001 10005 10012 10015 10022 10030; do
        ffmpeg -f lavfi -i color=c=white:s=320x240:d=1 -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='$id':fontsize=48:fontcolor=black:x=(w-text_w)/2:y=(h-text_h)/2" -c:v libx264 -y /tmp/vid_$id.mp4
    done

    cat > /tmp/list.txt <<EOF
file '/tmp/vid_10001.mp4'
file '/tmp/vid_10005.mp4'
file '/tmp/vid_10012.mp4'
file '/tmp/vid_10015.mp4'
file '/tmp/vid_10022.mp4'
file '/tmp/vid_10030.mp4'
EOF
    ffmpeg -f concat -safe 0 -i /tmp/list.txt -c copy /app/reference_video.mp4
    rm /tmp/vid_*.mp4 /tmp/list.txt

    # Generate the corrupted CSV
    cat > /app/data/export.csv <<EOF
event_id,parent_event_id,timestamp,event_type,payload
10000,,100,type,data
10001,10000,101,type,data
10005,10001,102,type,data
10012,10005,103,type,data
10015,10012,104,type,data
10022,10015,105,type,data
10030,10022,106,type,data
10001,10000,90,type,old_data
10005,10001,90,type,old_data
99999,99998,200,type,corrupted_data
EOF

    # Generate the reference oracle
    cat > /tmp/oracle.go <<'EOF'
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "sort"
)

type Query struct {
    Type    string `json:"type"`
    EventID string `json:"event_id"`
    Limit   int    `json:"limit"`
    Sort    string `json:"sort"`
}

func main() {
    if len(os.Args) < 2 {
        return
    }
    var queries []Query
    err := json.Unmarshal([]byte(os.Args[1]), &queries)
    if err != nil {
        return
    }

    parents := map[string]string{
        "10001": "10000",
        "10005": "10001",
        "10012": "10005",
        "10015": "10012",
        "10022": "10015",
        "10030": "10022",
    }
    timestamps := map[string]int{
        "10000": 100,
        "10001": 101,
        "10005": 102,
        "10012": 103,
        "10015": 104,
        "10022": 105,
        "10030": 106,
    }

    var results [][]string
    for _, q := range queries {
        var ans []string
        curr := q.EventID
        for {
            p, ok := parents[curr]
            if !ok || p == "" {
                break
            }
            ans = append(ans, p)
            curr = p
        }

        if q.Sort == "asc" {
            sort.Slice(ans, func(i, j int) bool { return timestamps[ans[i]] < timestamps[ans[j]] })
        } else {
            sort.Slice(ans, func(i, j int) bool { return timestamps[ans[i]] > timestamps[ans[j]] })
        }

        if len(ans) > q.Limit {
            ans = ans[:q.Limit]
        }
        if ans == nil {
            ans = []string{}
        }
        results = append(results, ans)
    }
    out, _ := json.Marshal(results)
    fmt.Println(string(out))
}
EOF
    go build -o /app/bin/reference_oracle /tmp/oracle.go
    rm /tmp/oracle.go

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user