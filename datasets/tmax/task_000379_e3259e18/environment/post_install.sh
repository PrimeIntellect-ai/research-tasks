apt-get update && apt-get install -y python3 python3-pip golang git
pip3 install pytest

mkdir -p /home/user/metric-calc
cd /home/user/metric-calc
git init
git config user.email "devops@example.com"
git config user.name "DevOps Engineer"

# Commit 1 (v1.0)
cat << 'EOF' > main.go
package main

import "fmt"

func CalcHealth(success, failed, total int) float64 {
	return (float64(success-failed) / float64(total)) * 100.0
}

func main() {
	fmt.Printf("Health: %f\n", CalcHealth(90, 10, 100))
}
EOF

cat << 'EOF' > main_test.go
package main

import "testing"

func TestCalcHealth(t *testing.T) {
	h := CalcHealth(90, 10, 100)
	if h != 80.0 {
		t.Fatalf("Expected 80.0, got %f", h)
	}
}
EOF

go mod init metric-calc
git add main.go main_test.go go.mod
git commit -m "Initial commit with correct formula"
git tag v1.0

# Commit 2
echo "// minor refactor" >> main.go
git commit -am "Minor comment addition"

# Commit 3 (The bad commit)
cat << 'EOF' > main.go
package main

import "fmt"

func CalcHealth(success, failed, total int) float64 {
	// BUG: Ignoring failed requests in calculation
	return (float64(success) / float64(total)) * 100.0
}

func main() {
	fmt.Printf("Health: %f\n", CalcHealth(90, 10, 100))
}
EOF
git commit -am "Update health calculation logic"
BAD_COMMIT=$(git rev-parse HEAD)
echo $BAD_COMMIT > /tmp/expected_bad_commit.sha

# Commit 4
echo "// added more logging context" >> main.go
git commit -am "Add logging context"

# Commit 5 (HEAD - Compiler Error)
cat << 'EOF' > main.go
package main

import "fmt"

func CalcHealth(success, failed, total int) float64 {
	// BUG: Ignoring failed requests in calculation
	return (float64(success) / float64(total)) * 100.0
}

func main() {
	// COMPILER ERROR: Missing comma
	fmt.Printf("Health: %f\n" CalcHealth(90, 10, 100))
}
EOF
git commit -am "Refactor main output"

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user