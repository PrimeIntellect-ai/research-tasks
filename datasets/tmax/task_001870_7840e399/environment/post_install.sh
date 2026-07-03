apt-get update && apt-get install -y python3 python3-pip golang espeak
    pip3 install pytest

    mkdir -p /app

    espeak -w /app/archiver_spec.wav "The custom configuration archive must begin with the magic bytes C O N F T R A C K 9 9. That is C, O, N, F, T, R, A, C, K, 9, 9 in ASCII. For the file paths in the headers, each path must be exactly 64 bytes long. If the path is shorter than 64 bytes, it must be right-padded with null bytes. If it is longer, you must truncate it to exactly 64 bytes."

    cat << 'EOF' > /tmp/oracle.go
package main

import (
	"bufio"
	"encoding/binary"
	"io"
	"os"
	"strconv"
	"strings"
	"syscall"
)

func padOrTruncate(s string, length int) []byte {
	b := make([]byte, length)
	copy(b, []byte(s))
	return b
}

func main() {
	if len(os.Args) < 2 {
		os.Exit(1)
	}
	lockFile := os.Args[1]
	f, err := os.OpenFile(lockFile, os.O_CREATE|os.O_RDWR, 0666)
	if err != nil {
		os.Exit(1)
	}
	defer f.Close()

	if err := syscall.Flock(int(f.Fd()), syscall.LOCK_EX); err != nil {
		os.Exit(1)
	}
	defer syscall.Flock(int(f.Fd()), syscall.LOCK_UN)

	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	defer writer.Flush()

	writer.Write([]byte("CONFTRACK99"))

	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				break
			}
			os.Exit(1)
		}
		line = strings.TrimSuffix(line, "\n")
		parts := strings.Split(line, " ")

		if parts[0] == "WRITE" {
			path := parts[1]
			size, _ := strconv.ParseUint(parts[2], 10, 64)
			writer.WriteByte('W')
			writer.Write(padOrTruncate(path, 64))
			binary.Write(writer, binary.LittleEndian, size)

			data := make([]byte, size)
			io.ReadFull(reader, data)
			writer.Write(data)
		} else if parts[0] == "HLINK" {
			target := parts[1]
			link := parts[2]
			writer.WriteByte('H')
			writer.Write(padOrTruncate(link, 64))
			writer.Write(padOrTruncate(target, 64))
		}
	}
}
EOF
    go build -o /app/oracle_archiver /tmp/oracle.go
    rm /tmp/oracle.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user