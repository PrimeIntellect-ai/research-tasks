apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        git \
        build-essential \
        cmake \
        wget \
        golang-go \
        espeak \
        ca-certificates

    pip3 install pytest

    # Create directories
    mkdir -p /app/data /opt/baseline /home/user

    # Generate audio file
    espeak "Hi, I'm calling about my recent bill. My customer ID is 88472. I need someone to look into my account." -w /app/call_audio.wav

    # Install whisper.cpp
    git clone https://github.com/ggerganov/whisper.cpp.git /opt/whisper
    cd /opt/whisper
    git checkout v1.5.4
    make
    bash ./models/download-ggml-model.sh base.en

    # Generate CSV files
    cat << 'EOF' > /tmp/gen_data.py
import csv
import random

random.seed(42)

with open('/app/data/agents.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['agent_id', 'department', 'rating'])
    depts = ['Billing', 'Support', 'Sales', 'Technical']
    for i in range(1, 10001):
        writer.writerow([i, random.choice(depts), round(random.uniform(1, 5), 1)])

with open('/app/data/tickets.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ticket_id', 'customer_id', 'agent_id', 'duration_mins'])
    for i in range(1, 500001):
        if i <= 5:
            cid = 88472
        else:
            cid = random.randint(10000, 99999)
        writer.writerow([i, cid, random.randint(1, 10000), random.randint(5, 120)])
EOF
    python3 /tmp/gen_data.py

    # Create naive Go script
    cat << 'EOF' > /home/user/analyze.go
package main

import (
	"encoding/csv"
	"encoding/json"
	"os"
	"strconv"
)

type Result struct {
	CustomerID  string                     `json:"customer_id"`
	Departments map[string]DepartmentStats `json:"departments"`
}

type DepartmentStats struct {
	TotalDuration int     `json:"total_duration"`
	AvgRating     float64 `json:"avg_rating"`
}

func main() {
	if len(os.Args) < 2 {
		return
	}
	customerID := os.Args[1]

	ticketsFile, _ := os.Open("/app/data/tickets.csv")
	defer ticketsFile.Close()
	ticketsReader := csv.NewReader(ticketsFile)
	tickets, _ := ticketsReader.ReadAll()

	agentsFile, _ := os.Open("/app/data/agents.csv")
	defer agentsFile.Close()
	agentsReader := csv.NewReader(agentsFile)
	agents, _ := agentsReader.ReadAll()

	deptTotals := make(map[string]int)
	deptRatings := make(map[string]float64)
	deptCounts := make(map[string]int)

	// Naive O(N^2) join
	for i := 1; i < len(tickets); i++ {
		for j := 1; j < len(agents); j++ {
			if tickets[i][1] == customerID && tickets[i][2] == agents[j][0] {
				dept := agents[j][1]
				dur, _ := strconv.Atoi(tickets[i][3])
				rating, _ := strconv.ParseFloat(agents[j][2], 64)

				deptTotals[dept] += dur
				deptRatings[dept] += rating
				deptCounts[dept]++
			}
		}
	}

	res := Result{
		CustomerID:  customerID,
		Departments: make(map[string]DepartmentStats),
	}

	for dept, count := range deptCounts {
		res.Departments[dept] = DepartmentStats{
			TotalDuration: deptTotals[dept],
			AvgRating:     deptRatings[dept] / float64(count),
		}
	}

	out, _ := json.MarshalIndent(res, "", "  ")
	os.WriteFile("/home/user/result.json", out, 0644)
}
EOF

    # Compile naive baseline
    cd /home/user
    go build -o /opt/baseline/analyze_naive analyze.go

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user