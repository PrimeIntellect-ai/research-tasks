apt-get update && apt-get install -y python3 python3-pip golang-go espeak
    pip3 install pytest

    mkdir -p /app

    # Generate audio file
    cat << 'EOF' > /app/transcript.txt
Okay, for the new custom dataset format. The file always begins with the magic bytes R A R C. 
After that, it's just a sequence of file entries until the end of the file.
For each file entry, first read a sixteen bit little endian integer which gives you the length of the file path.
Then read the file path string based on that length.
Next, read a thirty-two bit little endian integer for the file data size.
Then, you can just read or skip the actual file data for that many bytes.
Now for the critical security part: you must sanitize the paths. Resolve the archive path against the target directory. 
If the resulting absolute path falls strictly outside the target directory, you must reject it. Output the exact string 'WARN: ' followed by the raw original path from the archive.
If the path is safe and stays inside the target directory, output the exact string 'SAFE: ' followed by the fully resolved, cleaned absolute path.
EOF
    espeak -f /app/transcript.txt -w /app/dataset_notes.wav

    # Write oracle source
    cat << 'EOF' > /app/oracle.go
package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	if len(os.Args) != 3 {
		os.Exit(1)
	}
	archiveFile := os.Args[1]
	targetDir := os.Args[2]

	targetDirClean := filepath.Clean(targetDir)

	data, err := os.ReadFile(archiveFile)
	if err != nil {
		os.Exit(1)
	}

	reader := bytes.NewReader(data)

	magic := make([]byte, 4)
	if _, err := io.ReadFull(reader, magic); err != nil {
		os.Exit(1)
	}
	if string(magic) != "RARC" {
		os.Exit(1)
	}

	for {
		var pathLen uint16
		if err := binary.Read(reader, binary.LittleEndian, &pathLen); err != nil {
			if err == io.EOF {
				break
			}
			os.Exit(1)
		}

		pathBytes := make([]byte, pathLen)
		if _, err := io.ReadFull(reader, pathBytes); err != nil {
			os.Exit(1)
		}
		pathStr := string(pathBytes)

		var dataSize uint32
		if err := binary.Read(reader, binary.LittleEndian, &dataSize); err != nil {
			os.Exit(1)
		}

		if _, err := reader.Seek(int64(dataSize), io.SeekCurrent); err != nil {
			os.Exit(1)
		}

		fullPath := filepath.Join(targetDirClean, pathStr)
		rel, err := filepath.Rel(targetDirClean, fullPath)
		if err != nil || strings.HasPrefix(rel, "..") {
			fmt.Printf("WARN: %s\n", pathStr)
		} else {
			fmt.Printf("SAFE: %s\n", fullPath)
		}
	}
}
EOF

    # Compile oracle
    go build -o /app/oracle_extractor /app/oracle.go
    chmod +x /app/oracle_extractor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user