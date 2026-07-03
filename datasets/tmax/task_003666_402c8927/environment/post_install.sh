apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest

    mkdir -p /app/poly-eval
    mkdir -p /app/vendor/fastmath

    cat << 'EOF' > /app/vendor/fastmath/go.mod
module fastmath

go 1.18
EOF

    cat << 'EOF' > /app/vendor/fastmath/eval.go
package fastmath

import "fmt"

var memo = make(map[string]int64)

func Eval(x int8, coeffs []int8) int64 {
	key := fmt.Sprintf("%d-%v", x, coeffs)
	if val, ok := memo[key]; ok {
		return val
	}
	var res int64 = 0
	var pow int64 = 1
	for _, c := range coeffs {
		res += int64(c) * pow
		pow *= int64(x)
	}
	memo[key] = res
	return res
}
EOF

    cat << 'EOF' > /app/vendor/fastmath/parse.go
package fastmath

import "errors"

var ErrCorruptedFrame = errors.New("corrupted frame")

func ParseFrame(data []byte) (int8, []int8, int, error) {
	if len(data) == 0 {
		return 0, nil, 0, errors.New("EOF")
	}
	N := int(data[0])
	if len(data) < 2 {
		return 0, nil, 0, errors.New("EOF")
	}
	x := int8(data[1])
	// BUG: no bounds check for 2+N
	coeffs := make([]int8, N)
	for i := 0; i < N; i++ {
		coeffs[i] = int8(data[2+i])
	}
	return x, coeffs, 2 + N, nil
}
EOF

    cat << 'EOF' > /app/poly-eval/go.mod
module poly-eval

go 1.18

require fastmath v0.0.0
replace fastmath => ../vendor/fastmath
EOF

    cat << 'EOF' > /app/poly-eval/main.go
package main

import (
	"fastmath"
	"fmt"
	"io"
	"os"
	"sync"
)

func main() {
	data, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}

	var wg sync.WaitGroup
	offset := 0
	for offset < len(data) {
		x, coeffs, n, err := fastmath.ParseFrame(data[offset:])
		if err != nil {
			break
		}

		wg.Add(1)
		go func(x int8, coeffs []int8) {
			defer wg.Done()
			res := fastmath.Eval(x, coeffs)
			fmt.Printf("%d\n", res)
		}(x, coeffs)

		offset += n
	}
	wg.Wait()
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user