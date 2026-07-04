apt-get update && apt-get install -y python3 python3-pip golang ffmpeg git
    pip3 install pytest numpy

    mkdir -p /app/math-vid-service
    cd /app/math-vid-service

    git config --global user.email "engineer@example.com"
    git config --global user.name "Engineer"
    git init

    cat << 'EOF' > main.go
package main
import (
	"encoding/binary"
	"os"
	"math"
)

func main() {
	if len(os.Args) < 3 { return }
	outFile := os.Args[2]

	f, _ := os.Create(outFile)
	defer f.Close()

	for i := 0; i < 100; i++ {
		matrix := make([]float64, 100000)
		for j := 0; j < 100000; j++ {
			matrix[j] = math.Sin(float64(i+j))
		}

		for _, v := range matrix {
			binary.Write(f, binary.LittleEndian, v)
		}
	}
}
EOF

    go mod init math-vid-service
    git add main.go go.mod
    git commit -m "Initial commit with correct serialization"

    go build -o math-vid-service main.go
    ./math-vid-service /app/input_video.mp4 /app/ref_metrics.bin

    cat << 'EOF' > main.go
package main
import (
	"encoding/binary"
	"os"
	"math"
)

var GlobalFrameCache [][]float64

func main() {
	if len(os.Args) < 3 { return }
	outFile := os.Args[2]

	f, _ := os.Create(outFile)
	defer f.Close()

	for i := 0; i < 100; i++ {
		matrix := make([]float64, 100000)
		for j := 0; j < 100000; j++ {
			matrix[j] = math.Sin(float64(i+j))
		}

		GlobalFrameCache = append(GlobalFrameCache, matrix)

		for _, v := range matrix {
			binary.Write(f, binary.LittleEndian, int32(v))
		}
	}
}
EOF

    git add main.go
    git commit -m "Optimize processing and fix serialization types"

    ffmpeg -f lavfi -i testsrc=duration=1:size=320x240:rate=10 -c:v libx264 /app/input_video.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user