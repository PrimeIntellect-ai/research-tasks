apt-get update && apt-get install -y python3 python3-pip git golang build-essential
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # 1. Create the payload file
    cat << 'EOF' > /home/user/payload.txt
SGVsbG8gV29ybGQh/test+data=
EOF

    # 2. Setup the Git repo
    mkdir -p /home/user/data-parser
    cd /home/user/data-parser
    git init
    git branch -m main || git checkout -b main
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    # Create initial working code
    cat << 'EOF' > go.mod
module data-parser

go 1.18
EOF

    cat << 'EOF' > parser.go
package main

import (
	"encoding/base64"
	"fmt"
)

func DecodeData(input string) (string, error) {
	data, err := base64.StdEncoding.DecodeString(input)
	if err != nil {
		return "", fmt.Errorf("decoding error: %w", err)
	}
	return string(data), nil
}
EOF

    cat << 'EOF' > main.go
package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	filePath := flag.String("f", "", "file path")
	flag.Parse()

	if *filePath == "" {
		os.Exit(1)
	}

	content, err := os.ReadFile(*filePath)
	if err != nil {
		os.Exit(1)
	}

	res, err := DecodeData(string(content))
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("Decoded:", res)
}
EOF

    git add .
    git commit -m "Initial commit: working state"
    git tag v1.0.0

    # Generate 75 safe commits
    for i in {1..75}; do
        echo "// comment $i" >> main.go
        git commit -am "chore: update main.go ($i)"
    done

    # Introduce CGO dependency (needs CGO_ENABLED=1 and math library linking)
    # This creates a compilation requirement change mid-history.
    cat << 'EOF' > math_opt.go
package main

/*
#include <math.h>

double fast_pow(double a, double b) {
    return pow(a, b);
}
*/
import "C"

func optimize() {
    _ = C.fast_pow(2.0, 3.0)
}
EOF
    echo "func init() { optimize() }" >> main.go
    git add .
    git commit -m "feat: introduce CGO math optimizations"

    # Generate 45 safe commits
    for i in {76..120}; do
        echo "// comment $i" >> main.go
        git commit -am "chore: update main.go ($i)"
    done

    # INTRODUCE THE BUG (Regression Commit)
    cat << 'EOF' > parser.go
package main

import (
	"encoding/base64"
	"fmt"
)

func DecodeData(input string) (string, error) {
    // BUG: Changed from StdEncoding to URLEncoding
	data, err := base64.URLEncoding.DecodeString(input)
	if err != nil {
		return "", fmt.Errorf("decoding error: %w", err)
	}
	return string(data), nil
}
EOF
    git commit -am "refactor: use URLEncoding for base64 parsing"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Generate 50 safe commits
    for i in {121..170}; do
        echo "// comment $i" >> main.go
        git commit -am "chore: update main.go ($i)"
    done

    # Save the bad commit hash to a secure location for the test suite
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chown -R user:user /home/user/data-parser
    chown user:user /home/user/payload.txt
    chmod -R 777 /home/user