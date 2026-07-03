apt-get update && apt-get install -y python3 python3-pip golang-go
    pip3 install pytest

    # Create vendored package
    mkdir -p /app/vendor/go-rk45
    cat << 'EOF' > /app/vendor/go-rk45/go.mod
module rk45

go 1.18
EOF

    cat << 'EOF' > /app/vendor/go-rk45/integrator.go
package rk45

import "math"

func RK45Step(f func(float64, []float64) []float64, t float64, y []float64, dt float64) ([]float64, float64, float64) {
	k1 := f(t, y)

	y_tmp := make([]float64, len(y))
	for i := range y { y_tmp[i] = y[i] + dt*0.5*k1[i] }
	k2 := f(t + 0.5*dt, y_tmp)

	for i := range y { y_tmp[i] = y[i] + dt*0.5*k2[i] }
	k3 := f(t + 0.5*dt, y_tmp)

	for i := range y { y_tmp[i] = y[i] + dt*k3[i] }
	k4 := f(t + dt, y_tmp)

	y4 := make([]float64, len(y))
	for i := range y { y4[i] = y[i] + dt*(k1[i] + 2*k2[i] + 2*k3[i] + k4[i])/6.0 }

	y5 := make([]float64, len(y))
	for i := range y { y5[i] = y4[i] + dt*0.01*(k1[i]-k2[i]) }

	maxErr := 0.0
	for i := range y {
		// BUG: + instead of -
		diff := y5[i] + y4[i]
		if math.Abs(diff) > maxErr {
			maxErr = math.Abs(diff)
		}
	}

	return y4, maxErr, dt
}

func Integrate(f func(float64, []float64) []float64, t0, tf float64, y0 []float64, tol float64) ([][]float64, []float64) {
	t := t0
	y := y0
	dt := 0.01

	var history [][]float64
	var times []float64

	history = append(history, y)
	times = append(times, t)

	for t < tf {
		yNext, err, _ := RK45Step(f, t, y, dt)

		if err < tol {
			t += dt
			y = yNext
			history = append(history, y)
			times = append(times, t)
		}

		if err == 0 {
			dt *= 2
		} else {
			dt = dt * math.Pow(tol/err, 0.2)
		}
		if dt > 0.1 { dt = 0.1 }
		if dt < 1e-6 { dt = 1e-6 }
	}
	return history, times
}
EOF

    # Create user
    useradd -m -s /bin/bash user || true

    # Create simulator
    mkdir -p /home/user/simulator
    cat << 'EOF' > /home/user/simulator/go.mod
module simulator

go 1.18

require rk45 v0.0.0
replace rk45 => /app/vendor/go-rk45
EOF

    cat << 'EOF' > /home/user/simulator/main.go
package main

import (
	"fmt"
	"math"
	"os"
	"rk45"
)

func main() {
	f := func(t float64, y []float64) []float64 {
		r := math.Sqrt(y[0]*y[0] + y[1]*y[1])
		r3 := r * r * r
		return []float64{
			y[2],
			y[3],
			-y[0] / r3,
			-y[1] / r3,
		}
	}

	y0 := []float64{1.0, 0.0, 0.0, 1.0}

	history, times := rk45.Integrate(f, 0, 10.0, y0, 1e-6)

	file, err := os.Create("/home/user/dataset.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintf(file, "t,x,y,vx,vy,E\n")
	for i, y := range history {
		v2 := y[2]*y[2] + y[3]*y[3]
		r := math.Sqrt(y[0]*y[0] + y[1]*y[1])
		E := 0.5*v2 - 1.0/r
		fmt.Fprintf(file, "%f,%f,%f,%f,%f,%f\n", times[i], y[0], y[1], y[2], y[3], E)
	}
}
EOF

    chown -R user:user /app/vendor/go-rk45
    chown -R user:user /home/user/simulator
    chmod -R 777 /home/user