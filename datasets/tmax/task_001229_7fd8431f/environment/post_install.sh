apt-get update && apt-get install -y python3 python3-pip golang-go
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/conf_reader.go
package main

import (
	"encoding/binary"
	"encoding/json"
	"hash/crc32"
	"os"
)

type Entry struct {
	Type    uint8
	Content string
	Target  string
}

func main() {
	if len(os.Args) != 3 {
		return
	}
	inFile := os.Args[1]
	outFile := os.Args[2]

	data, err := os.ReadFile(inFile)
	if err != nil {
		return
	}

	outData := process(data)

	tmpFile := outFile + ".tmp"
	os.WriteFile(tmpFile, outData, 0644)
	os.Rename(tmpFile, outFile)
}

func process(data []byte) []byte {
	if len(data) < 8 {
		return []byte(`{"error": "bad_magic"}`)
	}
	if string(data[:4]) != "CARC" {
		return []byte(`{"error": "bad_magic"}`)
	}

	expectedCrc := binary.LittleEndian.Uint32(data[4:8])
	actualCrc := crc32.ChecksumIEEE(data[8:])
	if expectedCrc != actualCrc {
		return []byte(`{"error": "bad_crc"}`)
	}

	fs := make(map[string]Entry)
	paths := []string{}

	buf := data[8:]
	for len(buf) > 0 {
		typ := buf[0]
		pathLen := int(buf[1])
		path := string(buf[2 : 2+pathLen])
		buf = buf[2+pathLen:]

		if typ == 1 {
			cLen := int(binary.LittleEndian.Uint16(buf[:2]))
			content := string(buf[2 : 2+cLen])
			buf = buf[2+cLen:]
			fs[path] = Entry{Type: 1, Content: content}
		} else {
			tLen := int(buf[0])
			target := string(buf[1 : 1+tLen])
			buf = buf[1+tLen:]
			fs[path] = Entry{Type: 2, Target: target}
		}
		paths = append(paths, path)
	}

	result := make(map[string]string)
	for _, p := range paths {
		visited := make(map[string]bool)
		curr := p
		for {
			if visited[curr] {
				result[p] = "<LOOP>"
				break
			}
			visited[curr] = true

			ent, ok := fs[curr]
			if !ok {
				result[p] = "<BROKEN>"
				break
			}
			if ent.Type == 1 {
				result[p] = ent.Content
				break
			} else {
				curr = ent.Target
			}
		}
	}

	j, _ := json.Marshal(result)
	return j
}
EOF

    cd /app
    go build -ldflags="-s -w" -o conf_reader conf_reader.go
    rm conf_reader.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user