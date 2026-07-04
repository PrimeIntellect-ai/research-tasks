apt-get update && apt-get install -y python3 python3-pip golang-go imagemagick
    pip3 install pytest

    mkdir -p /app

    # Generate the image
    convert -background white -fill black -font Courier -pointsize 18 label:"DATA NORMALIZATION RULES\nColumn 1: Remove all non-digit characters.\nColumn 2: Convert to UPPERCASE. Replace all spaces (' ') with underscores ('_').\nColumn 3: Find the first contiguous digit sequence. If none exist, output '0'." /app/transformation_rules.png

    # Write oracle source code
    cat << 'EOF' > /app/oracle_src.go
package main

import (
	"encoding/csv"
	"io"
	"os"
	"regexp"
	"strings"
)

func main() {
	r := csv.NewReader(os.Stdin)
	r.FieldsPerRecord = 3
	r.LazyQuotes = true
	w := csv.NewWriter(os.Stdout)

	reCol1 := regexp.MustCompile(`[^\d]`)
	reCol3 := regexp.MustCompile(`\d+`)

	for {
		rec, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			continue
		}

		c1 := reCol1.ReplaceAllString(rec[0], "")
		c2 := strings.ReplaceAll(strings.ToUpper(rec[1]), " ", "_")
		c3 := reCol3.FindString(rec[2])
		if c3 == "" {
			c3 = "0"
		}

		w.Write([]string{c1, c2, c3})
	}
	w.Flush()
}
EOF

    # Compile the oracle
    cd /app
    go build -o oracle_parser oracle_src.go

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app