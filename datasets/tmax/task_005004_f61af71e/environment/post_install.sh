apt-get update && apt-get install -y python3 python3-pip git golang-go
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/repo
cd /home/user/repo
git init
git config user.name "Dev"
git config user.email "dev@example.com"

cat << 'EOF' > go.mod
module leaktest

go 1.20
EOF

cat << 'EOF' > main.go
package main

import (
	"context"
	"errors"
)

func ProcessData(ctx context.Context, data []byte) error {
	if len(data) == 0 {
		return errors.New("empty data")
	}
	// ... logic
	return nil
}
EOF

cat << 'EOF' > main_test.go
package main

import (
	"context"
	"runtime"
	"testing"
	"time"
)

func TestProcessDataLeak(t *testing.T) {
	initial := runtime.NumGoroutine()
	ctx, cancel := context.WithCancel(context.Background())
	ProcessData(ctx, []byte{})
	cancel()
	time.Sleep(10 * time.Millisecond)
	final := runtime.NumGoroutine()
	if final > initial {
		t.Fatalf("goroutine leak detected: %d > %d", final, initial)
	}
}
EOF

git add .
git commit -m "Initial commit"
GOOD_COMMIT=$(git rev-parse HEAD)

# Create good commits
for i in {1..25}; do
  echo "// comment $i" >> main.go
  git commit -am "Good commit $i"
done

# Inject bug at commit 26
cat << 'EOF' > main.go
package main

import (
	"context"
	"errors"
)

func leakyWorker(ctx context.Context, ch chan struct{}) {
	<-ch // blocks forever if not closed
}

func ProcessData(ctx context.Context, data []byte) error {
	if len(data) == 0 {
		ch := make(chan struct{})
		go leakyWorker(ctx, ch)
		return errors.New("empty data")
	}
	return nil
}
EOF

git commit -am "Add worker optimization"
BAD_COMMIT=$(git rev-parse HEAD)

# Create more bad commits
for i in {27..50}; do
  echo "// comment $i" >> main.go
  git commit -am "Bad commit $i"
done

# Create a test script
cat << 'EOF' > test.sh
#!/bin/bash
if [ "$CONFIG_PATH" != "/etc/app/config.json" ]; then
  echo "Error: CONFIG_PATH not set correctly"
  exit 125
fi
go test -v ./...
EOF
chmod +x test.sh
git add test.sh
git commit -m "Add test script"

# Create the dump file
cat << 'EOF' > /home/user/dump.txt
goroutine 1 [running]:
runtime/debug.Stack()
	/usr/local/go/src/runtime/debug/stack.go:24 +0x65
main.main()
	/home/user/repo/main.go:20 +0x45

goroutine 18 [chan receive]:
leaktest.leakyWorker(0x0?, 0x0?)
	/home/user/repo/main.go:9 +0x25
created by leaktest.ProcessData
	/home/user/repo/main.go:15 +0x78
EOF

# Write truth values for verification
echo "Commit: $BAD_COMMIT" > /tmp/expected_solution.txt
echo "Function: leaktest.leakyWorker" >> /tmp/expected_solution.txt

chmod -R 777 /home/user