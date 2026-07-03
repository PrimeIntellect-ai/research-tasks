You are a performance engineer profiling a bioinformatics application. 

We have a Go program located at `/home/user/gc_calc.go` that parses a FASTA file (`/home/user/data.fasta`) and calculates a weighted GC-content score for each sequence in parallel. 

Currently, the application produces slightly non-reproducible results across different runs. This happens because the sequence weights are sent over a channel and accumulated as they arrive. Due to non-deterministic goroutine execution order and the non-associative nature of floating-point arithmetic, the final sum varies slightly at the lowest precision levels.

Your task is to:
1. Modify `/home/user/gc_calc.go` so that the floating-point reduction order is strictly deterministic. Specifically, you must collect all the individual sequence weights from the channel into a slice, **sort them in ascending numerical order**, and *then* sequentially sum them up.
2. Ensure the output is printed to exactly 10 decimal places using `fmt.Printf("%.10f\n", totalWeight)`.
3. Run your fixed program and redirect its deterministic output to a file named `/home/user/fixed_result.txt`.

The FASTA file and the Go source code are already present in your home directory. You only need to use standard Go libraries. Do not change the logic of the `calcWeight` function.