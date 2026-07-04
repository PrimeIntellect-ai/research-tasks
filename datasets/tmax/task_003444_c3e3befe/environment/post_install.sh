apt-get update && apt-get install -y python3 python3-pip sqlite3 espeak wget tar build-essential
    pip3 install pytest

    # Install Go 1.21+ to satisfy github.com/mattn/go-sqlite3 requirements
    wget https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
    export PATH=/usr/local/go/bin:$PATH
    rm go1.21.6.linux-amd64.tar.gz

    mkdir -p /app
    cd /app

    # Generate the SQLite database
    sqlite3 /app/graph.db <<EOF
CREATE TABLE nodes(id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE edges(source_id INTEGER, target_id INTEGER);
CREATE INDEX idx_nodes_name ON nodes(name);
INSERT INTO nodes(id, name) VALUES (1, 'Alpha'), (2, 'Bravo'), (3, 'Charlie'), (4, 'Delta'), (5, 'Echo');
INSERT INTO edges(source_id, target_id) VALUES (1, 2), (1, 3), (2, 3), (4, 1), (5, 1), (3, 4);
EOF

    # Corrupt the index artificially
    python3 -c "
with open('/app/graph.db', 'r+b') as f:
    data = f.read()
    idx = data.find(b'idx_nodes_name')
    if idx != -1:
        f.seek(idx + 5)
        f.write(b'X')
"

    # Create the oracle
    cat << 'EOF' > /app/oracle_query_graph.go
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"strconv"

	_ "github.com/mattn/go-sqlite3"
)

type NodeScore struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Score int    `json:"score"`
}

func main() {
	if len(os.Args) != 4 {
		return
	}
	limit, _ := strconv.Atoi(os.Args[1])
	offset, _ := strconv.Atoi(os.Args[2])
	minScore, _ := strconv.Atoi(os.Args[3])

	db, err := sql.Open("sqlite3", "/app/graph.db")
	if err != nil {
		panic(err)
	}
	defer db.Close()

	query := `
		SELECT n.id, n.name,
		       (SELECT COUNT(*) FROM edges WHERE target_id = n.id) - 
		       (SELECT COUNT(*) FROM edges WHERE source_id = n.id) AS score
		FROM nodes n
		WHERE (SELECT COUNT(*) FROM edges WHERE target_id = n.id) - 
		      (SELECT COUNT(*) FROM edges WHERE source_id = n.id) >= ?
		ORDER BY score DESC, n.name ASC
		LIMIT ? OFFSET ?
	`
	rows, err := db.Query(query, minScore, limit, offset)
	if err != nil {
		panic(err)
	}
	defer rows.Close()

	var results []NodeScore
	for rows.Next() {
		var ns NodeScore
		if err := rows.Scan(&ns.ID, &ns.Name, &ns.Score); err != nil {
			panic(err)
		}
		results = append(results, ns)
	}

	if results == nil {
		results = []NodeScore{}
	}

	out, _ := json.Marshal(results)
	fmt.Println(string(out))
}
EOF

    # Build oracle
    go mod init oracle
    go get github.com/mattn/go-sqlite3
    go build -o /app/oracle_query_graph /app/oracle_query_graph.go

    # Generate the audio file
    espeak -w /app/requirements.wav "Calculate the node score by taking its in-degree and subtracting its out-degree. Sort the final results by the node score in descending order. If there is a tie, sort by the node name in ascending alphabetical order."

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user