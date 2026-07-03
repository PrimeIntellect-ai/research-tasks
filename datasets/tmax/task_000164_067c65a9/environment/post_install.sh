apt-get update && apt-get install -y python3 python3-pip git wget curl
    pip3 install pytest

    # Install Go 1.21.6
    wget -q https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
    export PATH=/usr/local/go/bin:$PATH
    rm go1.21.6.linux-amd64.tar.gz

    # Set up the vendored package
    mkdir -p /app/graph
    cd /app/graph
    git clone https://github.com/dominikbraun/graph.git .
    git checkout v0.23.0
    # Perturb the go.mod
    sed -i 's/^go .*/go 1.99/' go.mod

    # Build the oracle (hidden from agent)
    mkdir -p /opt/oracle/src
    cat << 'EOF' > /opt/oracle/src/main.go
package main

import (
	"fmt"
	"math/rand"
	"os"
	"sort"
	"strconv"

	"github.com/dominikbraun/graph"
)

func main() {
	if len(os.Args) != 3 {
		return
	}
	seq := os.Args[1]
	seed, _ := strconv.ParseInt(os.Args[2], 10, 64)

	if len(seq) < 3 {
		return
	}

	g := graph.New(graph.StringHash, graph.Directed())

	var kmers []string
	for i := 0; i <= len(seq)-3; i++ {
		kmers = append(kmers, seq[i:i+3])
		g.AddVertex(seq[i:i+3])
	}

	for i := 0; i < len(kmers)-1; i++ {
		g.AddEdge(kmers[i], kmers[i+1])
	}

	rand.Seed(seed)
	curr := kmers[0]

	for step := 0; step < 100; step++ {
		adj, _ := g.AdjacencyMap()
		edges := adj[curr]
		if len(edges) == 0 {
			break
		}
		var dests []string
		for dest := range edges {
			dests = append(dests, dest)
		}
		sort.Strings(dests)
		idx := rand.Intn(len(dests))
		curr = dests[idx]
	}
	fmt.Print(curr)
}
EOF
    cd /opt/oracle/src
    go mod init oracle
    go get github.com/dominikbraun/graph@v0.23.0
    go build -o /opt/oracle/simulate_oracle main.go

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user