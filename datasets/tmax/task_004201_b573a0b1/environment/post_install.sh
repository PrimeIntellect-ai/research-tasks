apt-get update && apt-get install -y python3 python3-pip golang file
    pip3 install pytest

    # Setup directories
    mkdir -p /home/user/legacy /home/user/data/raw_files/text /home/user/data/raw_files/logs /home/user/bin

    # Create the legacy Go script
    cat << 'EOF' > /home/user/legacy/sorter.go
package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"sync"
)

func worker(id int, jobs <-chan string, wg *sync.WaitGroup, baseDir string) {
	defer wg.Done()
	for file := range jobs {
		ext := strings.ToLower(filepath.Ext(file))
		fullPath := filepath.Join(baseDir, file)

		if ext == ".txt" {
			os.MkdirAll(filepath.Join(baseDir, "text"), 0755)
			os.Rename(fullPath, filepath.Join(baseDir, "text", file))
		} else if ext == ".log" {
			os.MkdirAll(filepath.Join(baseDir, "logs"), 0755)
			os.Rename(fullPath, filepath.Join(baseDir, "logs", file))
		} else if ext == ".tmp" {
			os.Remove(fullPath)
		}
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Missing directory argument")
		return
	}
	baseDir := os.Args[1]
	files, err := os.ReadDir(baseDir)
	if err != nil {
		fmt.Println(err)
		return
	}

	jobs := make(chan string, len(files))
	var wg sync.WaitGroup

	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go worker(w, jobs, &wg, baseDir)
	}

	for _, f := range files {
		if !f.IsDir() {
			jobs <- f.Name()
		}
	}
	close(jobs)
	wg.Wait()
}
EOF

    # Create sample files
    touch /home/user/data/raw_files/file1.txt
    touch /home/user/data/raw_files/file2.log
    touch /home/user/data/raw_files/file3.tmp
    touch /home/user/data/raw_files/file4.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user