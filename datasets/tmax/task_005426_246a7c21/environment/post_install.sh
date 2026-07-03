apt-get update && apt-get install -y python3 python3-pip golang-go git gawk
    pip3 install pytest

    mkdir -p /app

    # Clone gonum v0.13.0
    git clone --depth 1 --branch v0.13.0 https://github.com/gonum/gonum.git /app/gonum

    # Introduce the syntax error in stat.go
    gawk '/func Mean/{c=1} c && /return/{sub("return", "returnn"); c=0} 1' /app/gonum/stat/stat.go > /app/gonum/stat/stat_tmp.go
    mv /app/gonum/stat/stat_tmp.go /app/gonum/stat/stat.go

    # Create oracle program
    cat << 'EOF' > /app/oracle_process.go
package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
)

type Result struct {
	Category string  `json:"category"`
	Mean     float64 `json:"mean"`
	CILower  float64 `json:"ci_lower"`
	CIUpper  float64 `json:"ci_upper"`
}

func main() {
	r := csv.NewReader(os.Stdin)
	records, err := r.ReadAll()
	if err != nil {
		return
	}

	if len(records) == 0 {
		fmt.Println("[]")
		return
	}

	records = records[1:] // Skip header
	groups := make(map[string][]float64)

	for _, row := range records {
		if len(row) < 4 {
			continue
		}
		cat := row[0]
		x, err1 := strconv.ParseFloat(row[1], 64)
		y, err2 := strconv.ParseFloat(row[2], 64)
		z, err3 := strconv.ParseFloat(row[3], 64)

		if err1 != nil || err2 != nil || err3 != nil {
			continue
		}

		score := 0.5*x + 0.3*y + 0.2*z
		groups[cat] = append(groups[cat], score)
	}

	var results []Result
	for cat, scores := range groups {
		n := float64(len(scores))
		if n < 2 {
			continue
		}

		sum := 0.0
		for _, v := range scores {
			sum += v
		}
		mean := sum / n

		varianceSum := 0.0
		for _, v := range scores {
			varianceSum += (v - mean) * (v - mean)
		}
		stddev := math.Sqrt(varianceSum / (n - 1))

		ci := 1.96 * (stddev / math.Sqrt(n))

		results = append(results, Result{
			Category: cat,
			Mean:     math.Round(mean*10000) / 10000,
			CILower:  math.Round((mean-ci)*10000) / 10000,
			CIUpper:  math.Round((mean+ci)*10000) / 10000,
		})
	}

	sort.Slice(results, func(i, j int) bool {
		return results[i].Category < results[j].Category
	})

	if results == nil {
		results = []Result{}
	}

	out, _ := json.Marshal(results)
	fmt.Println(string(out))
}
EOF

    cd /app
    go mod init oracle
    go build -o /app/oracle_process /app/oracle_process.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user