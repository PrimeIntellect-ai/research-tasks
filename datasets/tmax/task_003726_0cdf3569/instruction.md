You are a performance engineer analyzing a high-performance scientific computing application written in Go. The application performs a domain decomposition to numerically integrate a Fourier series signal in parallel.

The team has reported a severe issue: the simulation produces non-reproducible results. Every time the program runs, the final computed integral differs slightly at the 13th to 15th decimal place. This is caused by a floating-point reduction order bug. Because floating-point addition is not associative, summing the partial results from the concurrent workers in the non-deterministic order they complete (via a channel) changes the final value.

Here is the buggy source code:

```go
// /home/user/integrate.go
package main

import (
	"fmt"
	"math"
	"sync"
)

func signal(x float64) float64 {
	sum := 0.0
	// Fourier series approximation
	for k := 1.0; k <= 100.0; k++ {
		sum += math.Sin(k*x) / k
	}
	return sum
}

func main() {
	N := 10000000
	G := 16
	a, b := 0.0, math.Pi
	dx := (b - a) / float64(N)

	ch := make(chan float64, G)
	var wg sync.WaitGroup

	chunk := N / G
	for i := 0; i < G; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			startIdx := id * chunk
			endIdx := startIdx + chunk
			if id == G-1 {
				endIdx = N
			}

			partial := 0.0
			for j := startIdx; j < endIdx; j++ {
				x1 := a + float64(j)*dx
				x2 := a + float64(j+1)*dx
				partial += (signal(x1) + signal(x2)) / 2.0 * dx
			}
			ch <- partial
		}(i)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	total := 0.0
	// BUG: Non-deterministic order of floating-point reduction
	for p := range ch {
		total += p
	}

	fmt.Printf("%.15f\n", total)
}
```

Your task is to fix this issue and profile the application:

1. **Fix the Go program**: Modify the Go code to ensure bit-for-bit reproducibility. The partial sums from the `G` goroutines must be collected and then summed sequentially in strict order of their chunk IDs (`0` to `15`). Save your fixed code to `/home/user/integrate_fixed.go`.
2. **Add CPU Profiling**: Integrate the standard Go `runtime/pprof` library into your fixed program to generate a CPU profile. The profile must be written to `/home/user/cpu.prof` during execution.
3. **Capture Partial Sums**: Modify the program so that right before computing the final total, it writes the ordered partial sums to a CSV file at `/home/user/partials.csv`. The file should have no header, and each line should be formatted exactly as `%d,%.15f` where the first value is the chunk ID (`0` to `15`) and the second is the partial sum.
4. **Execution and Output**: Run your fixed Go program. It should print the final deterministic integral to standard output. Save this exact string (the number printed with `%.15f` precision) into `/home/user/result.txt`.
5. **Experimental Data Visualization**: Write a Python script `/home/user/plot.py` that reads `/home/user/partials.csv` and generates a bar chart of the partial sums. Save the plot as a PNG image at `/home/user/partials.png`.

Ensure all files are created exactly at the specified paths. Do not change the integration parameters (`N=10000000`, `G=16`, `100` Fourier components) or the mathematical logic (Trapezoidal rule).