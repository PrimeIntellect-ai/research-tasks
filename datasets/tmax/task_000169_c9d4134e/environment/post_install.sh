apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

useradd -m -s /bin/bash user || true

# Setup Git Repo
mkdir -p /home/user/app-repo
cd /home/user/app-repo
git init
git config user.name "SRE"
git config user.email "sre@example.com"

# Commit 1
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    fmt.Println("Service starting...")
}
EOF
git add main.go
git commit -m "init project"

# Commit 2
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    fmt.Println("Service starting...")
    initMetrics()
}
func initMetrics() {}
EOF
git add main.go
git commit -m "add metrics stub"

# Commit 3 (The Bug)
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    fmt.Println("Service starting...")
    initMetrics()
    panic("SRE_CRITICAL_ERR: unhandled nil pointer dereference in metric collector worker pool")
}
func initMetrics() {}
EOF
git add main.go
git commit -m "implement metric collection worker pool"
BAD_COMMIT=$(git rev-parse HEAD)

# Commit 4
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    fmt.Println("Service starting...")
    // Adding logging
    initMetrics()
    panic("SRE_CRITICAL_ERR: unhandled nil pointer dereference in metric collector worker pool")
}
func initMetrics() {}
EOF
git add main.go
git commit -m "add logging to initialization"

# Commit 5
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    fmt.Println("Service starting v2...")
    // Adding logging
    initMetrics()
    panic("SRE_CRITICAL_ERR: unhandled nil pointer dereference in metric collector worker pool")
}
func initMetrics() {}
EOF
git add main.go
git commit -m "bump version"

# Create Crash Dump
mkdir -p /home/user
dd if=/dev/urandom of=/home/user/crash-dump.bin bs=1K count=512 2>/dev/null
echo "goroutine 1 [running]:" >> /home/user/crash-dump.bin
echo "panic: SRE_CRITICAL_ERR: unhandled nil pointer dereference in metric collector worker pool" >> /home/user/crash-dump.bin
echo "main.main()" >> /home/user/crash-dump.bin
echo "        /app/main.go:8 +0x39" >> /home/user/crash-dump.bin
dd if=/dev/urandom bs=1K count=512 >> /home/user/crash-dump.bin 2>/dev/null

# Save the expected result for verification
cat << EOF > /tmp/expected_report.txt
COMMIT_HASH:${BAD_COMMIT}
ERROR:SRE_CRITICAL_ERR: unhandled nil pointer dereference in metric collector worker pool
EOF

chmod -R 777 /home/user