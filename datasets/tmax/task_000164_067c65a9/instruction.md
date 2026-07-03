You are an AI assistant helping a computational biology researcher run a simulation of primer traversal on a molecular sequence graph. 

Your goal is to build a Go program that constructs a de Bruijn graph from a DNA sequence, performs a simulated random walk (representing a simplified MCMC sampling step for primer selection), and outputs the final state. 

We have provided a vendored third-party graph library at `/app/graph` (a clone of `github.com/dominikbraun/graph`). However, there is a known issue: the vendored package fails to compile because its `go.mod` was accidentally modified to require Go version `1.99`, which your environment does not support. 

Please accomplish the following:
1. Fix the vendored package at `/app/graph` so it can be compiled and used locally (downgrade the Go version in its `go.mod` to `1.21`).
2. Write a Go program at `/home/user/simulate.go` and compile it to `/home/user/simulate`.
3. The program must accept exactly two command-line arguments:
   - Arg 1: A DNA sequence string (containing only A, C, G, T).
   - Arg 2: An integer seed for the random number generator.
4. The program must do the following:
   - Parse the sequence into overlapping 3-mers (e.g., "ACGT" -> "ACG", "CGT").
   - Use the vendored graph library to construct a directed graph where nodes are unique 3-mers.
   - Add a directed edge from node $U$ to node $V$ if the last 2 characters of $U$ match the first 2 characters of $V$. (Only add edges that are present as adjacent 3-mers in the input sequence).
   - Initialize the Go `math/rand` pseudo-random number generator with the provided integer seed.
   - Start a random walk at the very first 3-mer of the input sequence.
   - Perform exactly 100 steps. In each step:
     a) Get all outgoing edges from the current node.
     b) If there are no outgoing edges, the walk terminates early.
     c) Sort the destination nodes of these outgoing edges alphabetically.
     d) Select the next node by computing `idx := rand.Intn(len(outgoing_edges))` and picking the destination node at `idx`.
   - After the 100 steps (or early termination), print the string value of the final 3-mer node to standard output (no newline required, but a single newline is acceptable).

Your program's output must exactly match a reference implementation for any randomly generated sequence and seed. The system is offline, so you must initialize your `go.mod` in `/home/user` and use a `replace` directive to point `github.com/dominikbraun/graph` to the local `/app/graph` directory.