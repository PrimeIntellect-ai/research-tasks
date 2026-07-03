apt-get update && apt-get install -y python3 python3-pip git golang
    pip3 install pytest

    mkdir -p /home/user/opt-repo
    cd /home/user/opt-repo
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    cat << 'EOF' > params.json
{
    "initial_guess": 3.0,
    "tolerance": 1e-6,
    "max_iter": 100
}
EOF

    cat << 'EOF' > main.go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"os"
)

type Params struct {
	InitialGuess float64 `json:"initial_guess"`
	Tolerance    float64 `json:"tolerance"`
	MaxIter      int     `json:"max_iter"`
}

func f(x float64) float64 {
	return x*x*x - 2*x - 5
}

func df(x float64) float64 {
	return 3*x*x - 2
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Missing params file")
		os.Exit(1)
	}

	data, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		fmt.Println("Error reading params:", err)
		os.Exit(1)
	}

	var p Params
	if err := json.Unmarshal(data, &p); err != nil {
		fmt.Println("Error parsing params:", err)
		os.Exit(1)
	}

	x := p.InitialGuess
	for i := 0; i < p.MaxIter; i++ {
		fx := f(x)
		if math.Abs(fx) < p.Tolerance {
			fmt.Printf("%.8f\n", x)
			return
		}

		dfx := df(x)
		if dfx == 0 {
			fmt.Println("Zero derivative")
			os.Exit(2)
		}

		x = x - fx/dfx
	}

	fmt.Println("Convergence failure")
	os.Exit(3)
}
EOF

    git add main.go params.json
    git commit -m "Initial commit"

    for i in $(seq 1 199); do
        echo "Update $i" > README.md
        git add README.md

        if [ "$i" -eq 142 ]; then
            sed -i 's/return 3\*x\*x - 2/return 3*x - 2/g' main.go
            git add main.go
            git commit -m "Update math logic $i"
            BAD_COMMIT=$(git rev-parse HEAD)
            echo $BAD_COMMIT > /tmp/expected_bad_commit.txt
        elif [ "$i" -eq 199 ]; then
            git rm params.json
            git commit -m "Clean up unused files $i"
        else
            git commit -m "Routine update $i"
        fi
    done

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user