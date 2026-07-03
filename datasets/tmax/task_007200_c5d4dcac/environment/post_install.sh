apt-get update && apt-get install -y python3 python3-pip gcc make golang-go
    pip3 install pytest

    mkdir -p /home/user/telemetry_pipeline/c_src
    mkdir -p /home/user/telemetry_pipeline/go_src
    mkdir -p /home/user/telemetry_pipeline/bin

    # 1. Create decoder.c (Bug: i++ instead of i+=2 in hex decoding loop)
    cat << 'EOF' > /home/user/telemetry_pipeline/c_src/decoder.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

uint32_t crc32_for_byte(uint32_t r) {
    for(int j = 0; j < 8; ++j)
        r = (r & 1? 0: (uint32_t)0xEDB88320L) ^ r >> 1;
    return r ^ (uint32_t)0xFF000000L;
}

uint32_t crc32(const void *data, size_t n_bytes) {
    uint32_t crc = 0;
    static uint32_t table[0x100];
    if(!*table)
        for(size_t i = 0; i < 0x100; ++i)
            table[i] = crc32_for_byte(i);
    for(size_t i = 0; i < n_bytes; ++i)
        crc = table[(uint8_t)crc ^ ((uint8_t*)data)[i]] ^ crc >> 8;
    return crc;
}

int hex_char_to_int(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return -1;
}

int main() {
    char line[256];
    while (fgets(line, sizeof(line), stdin)) {
        line[strcspn(line, "\n")] = 0;
        size_t len = strlen(line);
        if (len == 0) continue;

        // Data format: [HEX STRING]:[CRC32_HEX]
        char *colon = strchr(line, ':');
        if (!colon) continue;
        *colon = 0;
        char *hex_data = line;
        char *crc_str = colon + 1;

        size_t hex_len = strlen(hex_data);
        if (hex_len % 2 != 0) continue;

        uint8_t *decoded = malloc(hex_len / 2);
        // BUG: i++ instead of i+=2
        for (size_t i = 0; i < hex_len; i++) { 
            int high = hex_char_to_int(hex_data[i]);
            int low = hex_char_to_int(hex_data[i+1]);
            decoded[i/2] = (high << 4) | low;
        }

        uint32_t expected_crc = (uint32_t)strtoul(crc_str, NULL, 16);
        uint32_t actual_crc = crc32(decoded, hex_len / 2);

        if (actual_crc == expected_crc) {
            // Null terminate and print
            char *out = malloc((hex_len / 2) + 1);
            memcpy(out, decoded, hex_len / 2);
            out[hex_len / 2] = '\0';
            printf("%s\n", out);
            free(out);
        }
        free(decoded);
    }
    return 0;
}
EOF

    # 2. Create Makefile (Bug: Spaces instead of tabs, wrong output dir)
    cat << 'EOF' > /home/user/telemetry_pipeline/Makefile
all: bin/decoder

bin/decoder: c_src/decoder.c
    gcc -O2 -Wall c_src/decoder.c -o bin/decoder

clean:
    rm -f bin/decoder
EOF

    # 3. Create orchestrator.go (Bug: unclosed jobs channel)
    cat << 'EOF' > /home/user/telemetry_pipeline/go_src/orchestrator.go
package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"sync"
)

func worker(jobs <-chan string, results chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()

	cmd := exec.Command("../bin/decoder")
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return
	}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return
	}

	if err := cmd.Start(); err != nil {
		return
	}

	go func() {
		for j := range jobs {
			io.WriteString(stdin, j+"\n")
		}
		stdin.Close()
	}()

	scanner := bufio.NewScanner(stdout)
	for scanner.Scan() {
		results <- scanner.Text()
	}
	cmd.Wait()
}

func main() {
	file, err := os.Open("../input_data.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	jobs := make(chan string, 100)
	results := make(chan string, 100)
	var wg sync.WaitGroup

	for w := 1; w <= 3; w++ {
		wg.Add(1)
		go worker(jobs, results, &wg)
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		jobs <- scanner.Text()
	}

	// BUG: jobs channel is never closed
	// close(jobs)

	go func() {
		wg.Wait()
		close(results)
	}()

	for r := range results {
		fmt.Println(r)
	}
}
EOF

    # 4. Create expected.txt and input_data.txt
    cat << 'EOF' > /home/user/telemetry_pipeline/expected.txt
SENSOR_ALPHA_TEMP_45C
SENSOR_BETA_PRESSURE_1012
SENSOR_GAMMA_HUMIDITY_60
EOF

    cat << 'EOF' > /home/user/telemetry_pipeline/input_data.txt
53454e534f525f414c5048415f54454d505f343543:86E74BBE
53454e534f525f424554415f50524553535552455f31303132:1B378E56
53454e534f525f47414d4d415f48554d49444954595f3630:5E58A38B
42414444415441:00000000
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/telemetry_pipeline
    chmod -R 777 /home/user