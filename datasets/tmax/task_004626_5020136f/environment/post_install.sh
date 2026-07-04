apt-get update && apt-get install -y python3 python3-pip git golang-go
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/metrics-parser
    cd /home/user/metrics-parser
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"
    go mod init metrics-parser

    # Create initial good state
    cat << 'EOF' > parser.go
package parser

import (
	"strconv"
	"strings"
)

func ParseMetrics(data string) (map[string]float64, error) {
	result := make(map[string]float64)
	lines := strings.Split(data, "\n")

	for i := 0; i < len(lines); i++ {
		line := strings.TrimSpace(lines[i])
		if line == "" {
			continue
		}
		parts := strings.Split(line, "|")
		if len(parts) < 2 {
			continue
		}
		val, err := strconv.ParseFloat(parts[1], 64)
		if err != nil {
			continue
		}
		result[parts[0]] += val
	}
	return result, nil
}
EOF

    cat << 'EOF' > parser_test.go
package parser

import "testing"

func TestParseMetrics(t *testing.T) {
	data := "cpu_usage|45.2\nmem_usage|1024.5\ncpu_usage|10.0\n"
	res, err := ParseMetrics(data)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if res["cpu_usage"] != 55.2 {
		t.Errorf("Expected cpu_usage 55.2, got %v", res["cpu_usage"])
	}
}

func TestParseMetricsMalformed(t *testing.T) {
	data := "cpu_usage|45.2\nmalformed_line\nmem_usage|1024.5\n"
	res, _ := ParseMetrics(data)
	if res["cpu_usage"] != 45.2 {
		t.Errorf("Expected cpu_usage 45.2, got %v", res["cpu_usage"])
	}
}
EOF

    git add .
    git commit -m "Initial commit with working parser"
    git tag v1.0.0

    # Add a few dummy commits
    for i in {1..3}; do
        echo "// Dummy comment $i" >> parser.go
        git commit -am "Minor formatting $i"
    done

    # Introduce the BAD commit
    cat << 'EOF' > parser.go
package parser

import (
	"strconv"
	"strings"
)

func ParseMetrics(data string) (map[string]float64, error) {
	result := make(map[string]float64)
	lines := strings.Split(data, "\n")

	for i := 0; i <= len(lines); i++ {
		line := strings.TrimSpace(lines[i])
		if line == "" {
			continue
		}
		parts := strings.Split(line, "|")
		val, err := strconv.ParseFloat(parts[1], 64)
		if err != nil {
			continue
		}
		result[parts[0]] += val
	}
	return result, nil
}
EOF

    git commit -am "Refactor parsing loop for performance"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Add a few more dummy commits
    for i in {4..6}; do
        echo "// Additional comment $i" >> parser.go
        git commit -am "Update docs $i"
    done

    git tag v1.1.0
    git branch -M main

    # Write out the expected bad commit to a hidden file for test verification
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    chmod -R 777 /home/user