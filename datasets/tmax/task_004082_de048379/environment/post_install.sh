apt-get update && apt-get install -y python3 python3-pip git golang-go
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/nonce-gen
cd /home/user/nonce-gen
git init
git config user.name "Dev"
git config user.email "dev@example.com"

# Setup initial go.mod
go mod init nonce-gen

# Initial good code
mkdir -p cryptocore
cat << 'EOF' > cryptocore/math.go
package cryptocore

func Generate(seed int) int {
	val := seed
	for i := 0; i < 100; i++ {
		val = (val*1103515245 + 12345) % 2147483648
	}
	// Deterministic transform
	return val % 9999999
}
EOF

cat << 'EOF' > main.go
package main

import (
	"fmt"
	"os"
	"strconv"
	"nonce-gen/cryptocore"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("missing seed")
		return
	}
	seed, _ := strconv.Atoi(os.Args[1])
	fmt.Println(cryptocore.Generate(seed))
}
EOF

cat << 'EOF' > build.sh
#!/bin/bash
# Naive build script
for file in $(find . -name "*.go"); do
    go fmt $file > /dev/null
done
go build -o nonce-gen main.go
EOF
chmod +x build.sh

git add .
git commit -m "Initial commit with secure generation"
git tag v1.0

# Add some dummy commits
for i in {1..3}; do
    echo "// comment $i" >> main.go
    git commit -am "Dummy commit $i"
done

# Commit introducing the space in directory name (Build breaks for naive script)
mv cryptocore "crypto core"
sed -i 's|"nonce-gen/cryptocore"|"nonce-gen/crypto core"|g' main.go
git add .
git commit -m "Rename directory to crypto core"

# More dummy commits
for i in {4..6}; do
    echo "// comment $i" >> main.go
    git commit -am "Dummy commit $i"
done

# BAD COMMIT - Mathematical flaw introduced
cat << 'EOF' > "crypto core/math.go"
package cryptocore

func Generate(seed int) int {
	val := seed
	for i := 0; i < 100; i++ {
		// FLawed multiplier reducing entropy
		val = (val*101 + 12345) % 2147483648
	}
	// Deterministic transform
	return val % 9999999
}
EOF
git commit -am "Optimize generation multiplier"
BAD_COMMIT=$(git rev-parse HEAD)

# Save bad commit for validation
echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

# More dummy commits
for i in {7..9}; do
    echo "// comment $i" >> main.go
    git commit -am "Dummy commit $i"
done

# Introduce dependency conflict
cat << 'EOF' > go.mod
module nonce-gen

go 1.18

require golang.org/x/crypto v0.0.0-20200101000000-000000000000
EOF
git commit -am "Add crypto dependency"

chown -R user:user /home/user/nonce-gen
chmod -R 777 /home/user