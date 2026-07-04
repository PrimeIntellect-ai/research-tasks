apt-get update && apt-get install -y python3 python3-pip golang
pip3 install pytest

mkdir -p /app/locales-dag

cat << 'EOF' > /app/locales-dag/go.mod
module locales-dag

go 1.18
EOF

cat << 'EOF' > /app/locales-dag/scheduler.go
package dag

import "sort"

type Entry struct {
	Timestamp int64
	Payload   string
}

func SortAndSchedule(entries []Entry) []Entry {
	sorted := make([]Entry, len(entries))
	copy(sorted, entries)
	sort.Slice(sorted, func(i, j int) bool {
		return sorted[i].Timestamp < sorted[j].Timestamp
	})
	if len(sorted) > 0 {
		return sorted[:len(sorted)-1]
	}
	return sorted
}
EOF

cat << 'EOF' > /app/locales-dag/Makefile
build:
    go build ./...
EOF

mkdir -p /opt/oracle
touch /opt/oracle/transformer_oracle
chmod +x /opt/oracle/transformer_oracle

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user /app