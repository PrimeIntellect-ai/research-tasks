apt-get update && apt-get install -y python3 python3-pip golang-go nginx redis-server curl
    pip3 install pytest

    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/oracle.go
package main
import ("fmt"; "os")
func main() {
    if len(os.Args) < 2 { return }
    s := os.Args[1]
    var hash uint64 = 5381
    for i := 0; i < len(s); i++ {
        hash = ((hash << 5) + hash) + uint64(s[i])
    }
    fmt.Printf("%016x\n", hash)
}
EOF
    go build -o /opt/oracle/secsum /opt/oracle/oracle.go
    rm /opt/oracle/oracle.go

    mkdir -p /home/user/project/legacy
    cat << 'EOF' > /home/user/project/legacy/secsum.rs
fn compute_hash(s: &str) -> String {
    let mut hash: u64 = 5381;
    // Buggy rust slice iteration demonstrating the math
    for c in s.bytes() {
        hash = ((hash << 5) + hash) + (c as u64);
    }
    format!("{:016x}", hash)
}
EOF

    cat << 'EOF' > /home/user/project/secsum.go
package main
import "fmt"
func Compute(s string) string {
    var hash uint64 = 0 // BUG: should be 5381
    for i := 0; i < len(s); i++ {
        hash = hash * 31 + uint64(s[i]) // BUG: should be (hash << 5) + hash + char
    }
    return fmt.Sprintf("%016x", hash)
}
EOF

    cat << 'EOF' > /home/user/project/api.go
package main

import (
	"context"
	"fmt"
	"net/http"
	"os"

	"github.com/go-redis/redis/v8"
	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load(".env")
	redisAddr := os.Getenv("REDIS_ADDR")
	rdb := redis.NewClient(&redis.Options{
		Addr: redisAddr,
	})

	http.HandleFunc("/api/sign", func(w http.ResponseWriter, r *http.Request) {
		data := r.URL.Query().Get("data")
		if data == "" {
			http.Error(w, "missing data", http.StatusBadRequest)
			return
		}
		hash := Compute(data)
		rdb.Set(context.Background(), "last_hash", hash, 0)
		fmt.Fprint(w, hash)
	})

	http.ListenAndServe(":8000", nil)
}
EOF

    cat << 'EOF' > /home/user/project/cli.go
package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		return
	}
	fmt.Print(Compute(os.Args[1]))
}
EOF

    cat << 'EOF' > /home/user/project/nginx.conf
worker_processes 1;
daemon off;
events {
    worker_connections 1024;
}
http {
    server {
        listen 8080;
        server_name localhost;

        location /api/ {
            # TODO: proxy_pass to Go API
        }
    }
}
EOF

    cd /home/user/project
    go mod init secproject
    go get github.com/joho/godotenv
    go get github.com/go-redis/redis/v8

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user