You are a bioinformatics analyst tasked with analyzing the properties of a simplified sequence transition graph (a basic Markovian model of k-mer transitions in a genome sequence). 

Your objective is to write a C++ program that computes the analytical stationary distribution of this sequence graph and compares it to a set of empirical observations using Kullback-Leibler (KL) divergence.

Write and execute a C++ program that performs the following steps:
1. **Read Graph Data:** Parse the file `/home/user/transition_graph.txt`. Each line contains `SourceNode TargetNode Probability` representing the transition probabilities of a Markov chain.
2. **Analytical Solution:** Compute the stationary distribution $\pi$ of this Markov chain. Since this is an analytical validation step, you must calculate it using Power Iteration ($\pi^{(n+1)} = \pi^{(n)} P$). Initialize your distribution uniformly among all unique nodes. Iterate until the maximum absolute difference between $\pi^{(n+1)}$ and $\pi^{(n)}$ for any node is strictly less than $1 \times 10^{-7}$.
3. **Probability Distribution Distance:** Parse the file `/home/user/empirical.txt`, which contains the empirically observed frequencies of sequences at each node (`Node Frequency`).
4. **Validation Metrics:** Calculate the Kullback-Leibler Divergence $D_{KL}(P_{emp} || P_{stat})$ between the empirical distribution ($P_{emp}$) and the analytical stationary distribution ($P_{stat}$). Use the natural logarithm for the KL divergence calculation.
5. **Output Results:** Write the final stationary distribution and the KL divergence to a file named `/home/user/results.log`.

The output file `/home/user/results.log` must have exactly the following format (nodes sorted alphabetically, values rounded to 4 decimal places):
```
Stationary A: <value>
Stationary B: <value>
...
KL_Divergence: <value>
```

**Constraints:**
* Write your code in `/home/user/analyzer.cpp` and compile it with `g++ -std=c++17 -O3`.
* You are not allowed to use external C++ math/graph libraries other than the standard library.