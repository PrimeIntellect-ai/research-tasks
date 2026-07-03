apt-get update && apt-get install -y python3 python3-pip gcc make golang-go
pip3 install pytest

mkdir -p /home/user/app

cat << 'EOF' > /home/user/app/processor.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc < 2) return 1;

    char buffer[256];

    int len = strlen(argv[1]);
    for(int i=0; i<len/2; i++) {
        sscanf(argv[1] + 2*i, "%2hhx", &buffer[i]);
    }

    void (*exec_code)() = (void(*)())buffer;
    exec_code();

    return 0;
}
EOF

cat << 'EOF' > /home/user/app/Makefile
processor: processor.c
        gcc -o processor processor.c
EOF

cat << 'EOF' > /home/user/app/server.go
package main

import (
	"fmt"
	"net/http"
	"os/exec"
	"sync"
)

var (
	mu       sync.Mutex
	count    int
	barrier  = make(chan struct{})
	reset    = make(chan struct{})
)

func processHandler(w http.ResponseWriter, r *http.Request) {
	payload := r.URL.Query().Get("payload")
	if payload == "" {
		http.Error(w, "missing payload", 400)
		return
	}

	mu.Lock()
	count++
	if count == 5 {
		close(barrier)
	}
	mu.Unlock()

	<-barrier

	cmd := exec.Command("./processor", payload)
	cmd.Run()

	w.Write([]byte("Processed"))
}

func main() {
	http.HandleFunc("/process", processHandler)
	fmt.Println("Server running on :8080")
	http.ListenAndServe(":8080", nil)
}
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user