apt-get update && apt-get install -y python3 python3-pip golang
    pip3 install pytest

    mkdir -p /app/distmetric
    mkdir -p /home/user

    cat << 'EOF' > /app/distmetric/go.mod
module github.com/scicompp/distmetric

go 1.18
EOF

    cat << 'EOF' > /app/distmetric/kl.go
package distmetric

import "math"

// KLDivergence computes the Kullback-Leibler divergence between two distributions.
func KLDivergence(p, q []float64) float64 {
	var sum float64
	for i := range p {
		if p[i] > 0 && q[i] > 0 {
			sum += p[i] * math.Log(q[i]/p[i])
		}
	}
	return sum
}
EOF

    # Generate the observed data
    python3 -c "
import random
with open('/home/user/observed_data.txt', 'w') as f:
    for _ in range(10000):
        f.write(f'{random.gauss(6.2, 2.5)}\n')
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app