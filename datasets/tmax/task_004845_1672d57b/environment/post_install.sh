apt-get update && apt-get install -y python3 python3-pip git golang
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/math-solver
cd /home/user/math-solver
git init
git config user.name "Dev"
git config user.email "dev@example.com"

# Commits 1 to 50 (Good)
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    sum := 0.0
    for i := 0; i < 100000; i++ {
        term := 1.0 / float64(2*i + 1)
        if i%2 != 0 { term = -term }
        sum += term
    }
    fmt.Printf("%.10f\n", sum*4)
}
EOF
git add main.go
git commit -m "Initial commit"
git tag v1.0

for i in $(seq 1 50); do
    echo "// refactor $i" >> main.go
    git commit -am "Refactor $i"
done

# Commit 51: Introduce precision loss (The Bad Commit)
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    var sum float32 = 0.0
    for i := 0; i < 100000; i++ {
        term := float32(1.0) / float32(2*i + 1)
        if i%2 != 0 { term = -term }
        sum += term
    }
    fmt.Printf("%.10f\n", sum*4)
}
EOF
git commit -am "Optimize memory usage"
BAD_COMMIT=$(git rev-parse HEAD)

# Commits 52 to 100 (Bad logic)
for i in $(seq 52 100); do
    echo "// update $i" >> main.go
    git commit -am "Update $i"
done

# Commits 101 to 120 (Build Failure + Bad Logic)
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    var sum float32 = 0.0
    for i := 0; i < 100000; i++ {
        term := float32(1.0) / float32(2*i + 1)
        if i%2 != 0 { term = -term }
        sum += term
    // missing brace syntax error
    fmt.Printf("%.10f\n", sum*4)
}
EOF
for i in $(seq 101 120); do
    echo "// feature $i" >> main.go
    git commit -am "Feature $i"
done

# Commits 121 to 200 (Fix Build, still Bad Logic)
cat << 'EOF' > main.go
package main
import "fmt"
func main() {
    var sum float32 = 0.0
    for i := 0; i < 100000; i++ {
        term := float32(1.0) / float32(2*i + 1)
        if i%2 != 0 { term = -term }
        sum += term
    }
    fmt.Printf("%.10f\n", sum*4)
}
EOF
for i in $(seq 121 200); do
    echo "// polish $i" >> main.go
    git commit -am "Polish $i"
done

# Save the target SHA for verification
echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

chown -R user:user /home/user/math-solver
chmod -R 777 /home/user