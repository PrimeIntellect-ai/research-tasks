apt-get update && apt-get install -y python3 python3-pip wget gcc sqlite3
    pip3 install pytest

    # Install Go
    wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz
    rm go1.21.0.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin

    useradd -m -s /bin/bash user || true

    # 1. Database Setup
    sqlite3 /home/user/dataset.sqlite << 'EOF'
CREATE TABLE papers (id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE citations (source_id INTEGER, target_id INTEGER);

WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt WHERE x<5000)
INSERT INTO papers(id, title) SELECT x, 'Paper ' || x FROM cnt;

WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt WHERE x<20000)
INSERT INTO citations(source_id, target_id) SELECT abs(random() % 5000) + 1, abs(random() % 5000) + 1 FROM cnt;

-- Create a corrupted/partial index that looks like a full index
CREATE INDEX idx_citations_source ON citations(source_id) WHERE source_id % 2 = 0;
PRAGMA writable_schema = 1;
UPDATE sqlite_master SET sql = 'CREATE INDEX idx_citations_source ON citations(source_id)' WHERE name = 'idx_citations_source';
PRAGMA writable_schema = 0;
EOF

    # 2. Oracle Program Setup
    mkdir -p /opt/oracle/src
    cd /opt/oracle/src
    go mod init oracle
    go get github.com/mattn/go-sqlite3
    cat << 'EOF' > main.go
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strconv"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	if len(os.Args) != 4 { os.Exit(1) }
	dbPath := os.Args[1]
	rootID, _ := strconv.Atoi(os.Args[2])
	maxDepth, _ := strconv.Atoi(os.Args[3])

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil { os.Exit(1) }
	defer db.Close()

	query := `
	WITH RECURSIVE cte(paper_id, depth) AS (
		SELECT ?, 0
		UNION ALL
		SELECT c.target_id, cte.depth + 1
		FROM cte
		JOIN citations c ON cte.paper_id = c.source_id
		WHERE cte.depth < ?
	)
	SELECT DISTINCT paper_id FROM cte;
	`
	rows, err := db.Query(query, rootID, maxDepth)
	if err != nil { os.Exit(1) }
	defer rows.Close()

	var ids []int
	for rows.Next() {
		var id int
		if err := rows.Scan(&id); err == nil { ids = append(ids, id) }
	}
	sort.Ints(ids)
	b, _ := json.Marshal(ids)
	fmt.Println(string(b))
}
EOF
    go build -o /opt/oracle/kg-export-oracle main.go

    # 3. Vendored Package Setup
    mkdir -p /app/kg-exporter-1.0.0
    cd /app/kg-exporter-1.0.0
    go mod init kg-exporter
    go get github.com/mattn/go-sqlite3
    go mod vendor
    cat << 'EOF' > main.go
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strconv"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	if len(os.Args) != 4 { os.Exit(1) }
	dbPath := os.Args[1]
	rootID, _ := strconv.Atoi(os.Args[2])
	maxDepth, _ := strconv.Atoi(os.Args[3])

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil { os.Exit(1) }
	defer db.Close()

	// PERTURBED QUERY: traverses backward
	query := `
	WITH RECURSIVE cte(paper_id, depth) AS (
		SELECT ?, 0
		UNION ALL
		SELECT c.target_id, cte.depth + 1
		FROM cte
		JOIN citations c ON cte.paper_id = c.target_id
		WHERE cte.depth < ?
	)
	SELECT DISTINCT paper_id FROM cte;
	`
	rows, err := db.Query(query, rootID, maxDepth)
	if err != nil { os.Exit(1) }
	defer rows.Close()

	var ids []int
	for rows.Next() {
		var id int
		if err := rows.Scan(&id); err == nil { ids = append(ids, id) }
	}
	sort.Ints(ids)
	b, _ := json.Marshal(ids)
	fmt.Println(string(b))
}
EOF

    # PERTURBED MAKEFILE: CGO_ENABLED=0 prevents sqlite3 build
    cat << 'EOF' > Makefile
all: build

build:
	CGO_ENABLED=0 go build -mod=vendor -o kg-export main.go
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app/kg-exporter-1.0.0