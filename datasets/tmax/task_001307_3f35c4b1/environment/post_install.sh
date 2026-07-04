apt-get update && apt-get install -y python3 python3-pip git golang
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/go-parser
    cd /home/user/go-parser

    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    # Create the test input
    echo -e "record_1\nrecord_2\nCORRUPT_RECORD\nrecord_4\nrecord_5" > input.csv
    git add input.csv

    # Create the initial GOOD Go file
    cat << 'EOF' > main.go
package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	b, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}

	for _, line := range strings.Split(string(b), "\n") {
		if strings.Contains(line, "CORRUPT") {
			// Safely skip corrupted records
			continue
		}
	}
	fmt.Println("Success")
}
EOF

    git add main.go
    git commit -m "Initial commit"

    # Create 80 good commits
    for i in $(seq 1 80); do
        echo "// Refactoring step $i" >> main.go
        git commit -am "chore: refactoring step $i"
    done

    # Introduce the BAD commit (intermittent failure on corrupted input)
    cat << 'EOF' > main.go
package main

import (
	"fmt"
	"os"
	"strings"
	"time"
)

func main() {
	b, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}

	for _, line := range strings.Split(string(b), "\n") {
		if strings.Contains(line, "CORRUPT") {
			// BUG: Intermittent panic when encountering corrupted data
			if time.Now().UnixNano()%5 == 0 {
				panic("unexpected nil pointer dereference on corrupted data")
			}
			continue
		}
	}
	fmt.Println("Success")
}
EOF

    echo "// Feature: async processing framework" >> main.go
    git commit -am "feat: implement new processing framework"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Save the bad commit hash somewhere hidden for the verification script
    echo -n $BAD_COMMIT > /tmp/.golden_bad_commit

    # Create 70 more commits so the bug is buried
    for i in $(seq 81 150); do
        echo "// Refactoring step $i" >> main.go
        git commit -am "chore: refactoring step $i"
    done

    chmod -R 777 /home/user