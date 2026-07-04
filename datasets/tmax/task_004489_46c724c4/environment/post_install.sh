apt-get update && apt-get install -y python3 python3-pip git golang-go
pip3 install pytest

mkdir -p /home/user/app
cd /home/user/app
git init

cat << 'EOF' > data.json
[
  {"name": "Widget", "qty": 10, "price": 15.50, "discount": 0.10},
  {"name": "Gadget", "qty": 5, "price": 42.00, "discount": 0.05}
]
EOF

cat << 'EOF' > processor.go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
)

type Item struct {
	Name     string  `json:"name"`
	Qty      int     `json:"qty"`
	Price    float64 `json:"price"`
	Discount float64 `json:"discount"`
}

type Result struct {
	Name  string  `json:"total_name"`
	Total float64 `json:"total_price"`
}

func process(items []Item) []Result {
	var results []Result
	for _, i := range items {
		// Calculate total
		total := float64(i.Qty) * i.Price * (1.0 - i.Discount)
		results = append(results, Result{Name: i.Name, Total: total})
	}
	return results
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: go run processor.go <input> <output>")
		os.Exit(1)
	}
	data, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	var items []Item
	json.Unmarshal(data, &items)

	results := process(items)

	out, _ := json.MarshalIndent(results, "", "  ")
	ioutil.WriteFile(os.Args[2], out, 0644)
}
EOF

git config user.email "test@example.com"
git config user.name "Test User"
git add data.json processor.go
git commit -m "Initial commit"
git tag v1.0

# Generate 200 commits
for i in $(seq 1 200); do
    echo "// Dummy comment $i" >> dummy.go
    git add dummy.go

    if [ $i -eq 134 ]; then
        # Introduce the regression
        sed -i 's/(1.0 - i.Discount)/(1.0 + i.Discount)/g' processor.go
        git add processor.go
    fi

    git commit -m "Commit $i"
done

# Save the bad commit hash for verification
git log --format="%H" --grep="Commit 134" > /tmp/expected_bad_commit.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user/app
chmod -R 777 /home/user