apt-get update && apt-get install -y python3 python3-pip golang-go ffmpeg
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user/ticket_4092

    # Create oracle Go source
    cat << 'EOF' > /app/oracle.go
package main

import (
	"encoding/binary"
	"fmt"
	"io"
	"os"
)

func main() {
	var index int
	for {
		var val uint64
		err := binary.Read(os.Stdin, binary.LittleEndian, &val)
		if err == io.EOF {
			break
		}
		if err != nil {
			break
		}
		if val > 200 {
			fmt.Println(index)
		}
		index++
	}
}
EOF

    # Compile oracle
    go build -o /app/oracle_detector /app/oracle.go
    rm /app/oracle.go

    # Create broken Go source
    cat << 'EOF' > /home/user/ticket_4092/main.go
package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	var index int
	for {
		var val uint64
		err := binary.Read(os.Stdin, binary.LittleEndian, &val)
		if err == io.EOF {
			break
		}
		if err != nil {
			break
		}
		if val > 200 {
			fmt.Println(index)
		}
		index++
	}
}
EOF

    # Generate video with a white flash at frames 145, 146, 147
    ffmpeg -f lavfi -i "color=c=black:s=64x64:r=30:d=10" -vf "drawbox=x=0:y=0:w=64:h=64:color=white:t=fill:enable='between(n,145,147)'" -c:v libx264 -y /app/server_room_cam.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user