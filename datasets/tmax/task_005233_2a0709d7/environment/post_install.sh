apt-get update && apt-get install -y python3 python3-pip curl golang-go
pip3 install pytest

mkdir -p /app/services

# Create the oracle Go implementation
cat << 'EOF' > /app/oracle.go
package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"hash/fnv"
	"os"
	"regexp"
	"strings"
)

type Output struct {
	ID       string         `json:"id"`
	Features map[string]int `json:"features"`
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	re := regexp.MustCompile(`[^a-z0-9\s]+`)

	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.SplitN(line, ",", 2)
		if len(parts) < 2 {
			continue
		}
		id := parts[0]
		text := parts[1]

		text = strings.ToLower(text)
		text = re.ReplaceAllString(text, "")

		tokens := strings.Fields(text)

		features := make(map[string]int)
		for _, token := range tokens {
			if len(token) > 0 {
				h := fnv.New32a()
				h.Write([]byte(token))
				hash := h.Sum32()
				bucket := hash % 256
				bucketStr := fmt.Sprintf("%d", bucket)
				features[bucketStr]++
			}
		}

		if len(features) > 0 {
			out := Output{
				ID:       id,
				Features: features,
			}
			b, _ := json.Marshal(out)
			fmt.Println(string(b))
		} else {
            // output empty features if no valid tokens
            out := Output{
				ID:       id,
				Features: make(map[string]int),
			}
			b, _ := json.Marshal(out)
			fmt.Println(string(b))
        }
	}
}
EOF

cd /app && go build -o oracle_cleaner oracle.go && rm oracle.go

# Create source.py
cat << 'EOF' > /app/services/source.py
import http.server
import socketserver
import uuid
import random
import string

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream':
            self.send_response(200)
            self.send_header('Content-type', 'text/csv')
            self.end_headers()
            for _ in range(100):
                text = ''.join(random.choices(string.ascii_letters + string.digits + " ,.", k=50))
                self.wfile.write(f"{uuid.uuid4()},{text}\n".encode())
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(('127.0.0.1', 8081), Handler) as httpd:
    httpd.serve_forever()
EOF

# Create sink.py
cat << 'EOF' > /app/services/sink.py
import http.server
import socketserver

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/ingest':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                with open('/tmp/sink.log', 'ab') as f:
                    f.write(post_data)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

with socketserver.TCPServer(('127.0.0.1', 8082), Handler) as httpd:
    httpd.serve_forever()
EOF

# Create worker.sh
cat << 'EOF' > /app/services/worker.sh
#!/bin/bash
source /app/pipeline.env
curl -s $SOURCE_URL | /home/user/cleaner | curl -s -X POST -H "Content-Type: application/json" --data-binary @- $SINK_URL
EOF

# Create start_pipeline.sh
cat << 'EOF' > /app/start_pipeline.sh
#!/bin/bash
python3 /app/services/source.py &
SOURCE_PID=$!
python3 /app/services/sink.py &
SINK_PID=$!

sleep 2
/app/services/worker.sh

kill $SOURCE_PID
kill $SINK_PID
EOF

# Create pipeline.env with bogus ports
cat << 'EOF' > /app/pipeline.env
SOURCE_URL=http://127.0.0.1:9991/stream
SINK_URL=http://127.0.0.1:9992/ingest
EOF

chmod +x /app/services/worker.sh
chmod +x /app/start_pipeline.sh

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app