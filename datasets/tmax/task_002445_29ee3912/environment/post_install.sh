apt-get update && apt-get install -y python3 python3-pip git golang jq
pip3 install pytest

mkdir -p /home/user/fin-aggregator/data

# Generate data/input.json
echo '[{"id": 1, "amount": 10000000.00}' > /home/user/fin-aggregator/data/input.json
for i in $(seq 2 100001); do
  echo ",{\"id\": $i, \"amount\": 0.50}" >> /home/user/fin-aggregator/data/input.json
done
echo ']' >> /home/user/fin-aggregator/data/input.json

# Create go.mod
cat << 'EOF' > /home/user/fin-aggregator/go.mod
module fin-aggregator

go 1.18
EOF

# Create aggregator.go (Initial Good Version)
cat << 'EOF' > /home/user/fin-aggregator/aggregator.go
package main

type Record struct {
	ID     int     `json:"id"`
	Amount float64 `json:"amount"`
}

func Aggregate(records []Record) float64 {
	var total float64 = 0.0
	for _, r := range records {
		total += r.Amount
	}
	return total
}
EOF

# Create main.go
cat << 'EOF' > /home/user/fin-aggregator/main.go
package main

import (
	"encoding/json"
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: fin-aggregator <input.json>")
		os.Exit(1)
	}
	data, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	var records []Record
	if err := json.Unmarshal(data, &records); err != nil {
		panic(err)
	}
	fmt.Printf("%.2f\n", Aggregate(records))
}
EOF

# Create aggregator_test.go
cat << 'EOF' > /home/user/fin-aggregator/aggregator_test.go
package main

import (
	"testing"
)

func TestAggregate(t *testing.T) {
	records := []Record{
		{ID: 1, Amount: 10000000.00},
	}
	for i := 0; i < 100000; i++ {
		records = append(records, Record{ID: i + 2, Amount: 0.50})
	}

	expected := 10050000.00
	result := Aggregate(records)

	if result != expected {
		t.Fatalf("Numerical instability detected: expected %.2f, got %.2f", expected, result)
	}
}
EOF

# Git Setup Script
cd /home/user/fin-aggregator
git init
git config user.email "test@example.com"
git config user.name "Test User"
git add .
git commit -m "Initial commit (good)"

# Make 3 dummy commits
for i in $(seq 1 3); do
  echo "// dummy $i" >> main.go
  git commit -am "Dummy commit $i"
done

# Introduce the bug (Bad Commit)
cat << 'EOF' > aggregator.go
package main

type Record struct {
	ID     int     `json:"id"`
	Amount float64 `json:"amount"`
}

func Aggregate(records []Record) float64 {
	var total float32 = 0.0 // Memory optimization
	for _, r := range records {
		total += float32(r.Amount)
	}
	return float64(total)
}
EOF
git commit -am "Optimize memory usage during aggregation"
BAD_COMMIT=$(git rev-parse HEAD)

# Make 3 more dummy commits
for i in $(seq 4 6); do
  echo "// dummy $i" >> main.go
  git commit -am "Dummy commit $i"
done

# Save the bad commit hash for verification
echo "$BAD_COMMIT" > /tmp/bad_commit_hash.txt

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user