apt-get update && apt-get install -y python3 python3-pip git golang-go
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/geo-transform
cd /home/user/geo-transform
git init
git config user.name "Dev"
git config user.email "dev@example.com"

# Good code: float64 precision
cat << 'EOF' > main.go
package main
import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)
func main() {
    file, _ := os.Open(os.Args[1])
    defer file.Close()
    scanner := bufio.NewScanner(file)
    var sum float64
    for scanner.Scan() {
        val := strings.TrimSpace(scanner.Text())
        if val == "" { continue }
        f, _ := strconv.ParseFloat(val, 64)
        sum += f
    }
    fmt.Printf("%.8f\n", sum)
}
EOF

git add main.go
git commit -m "Initial commit"
git tag v1.0

# 20 good commits
for i in {1..20}; do
    echo "// minor change $i" >> main.go
    git commit -am "Commit $i"
done

# The Bad commit: downcasting to float32 internally (precision loss)
cat << 'EOF' > main.go
package main
import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)
func main() {
    file, _ := os.Open(os.Args[1])
    defer file.Close()
    scanner := bufio.NewScanner(file)
    var sum float64
    for scanner.Scan() {
        val := strings.TrimSpace(scanner.Text())
        if val == "" { continue }
        f, _ := strconv.ParseFloat(val, 32)
        sum += float64(f)
    }
    fmt.Printf("%.8f\n", sum)
}
EOF
git commit -am "Refactor parsing to use 32-bit floats for memory efficiency"
BAD_COMMIT=$(git rev-parse HEAD)
echo "$BAD_COMMIT" > /home/user/expected_bad_commit.txt

# 19 more bad commits
for i in {21..39}; do
    echo "// minor change $i" >> main.go
    git commit -am "Commit $i"
done

git tag v2.0

# Generate input test data
cat << 'EOF' > /home/user/input.txt
12.34567891
98.76543219
0.00000001
EOF

chmod -R 777 /home/user