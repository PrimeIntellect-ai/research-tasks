# test_final_state.py

import os
import subprocess
import tempfile

def test_go_file_exists():
    assert os.path.isfile('/home/user/evaluate_distribution.go'), "Missing /home/user/evaluate_distribution.go"

def test_pipeline_script_exists():
    assert os.path.isfile('/home/user/pipeline.sh'), "Missing /home/user/pipeline.sh"

def test_pipeline_execution_and_output():
    # Run the student's pipeline
    result = subprocess.run(['bash', '/home/user/pipeline.sh'], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with return code {result.returncode}\nStderr: {result.stderr}"

    out_csv = '/home/user/tvd_convergence.csv'
    assert os.path.isfile(out_csv), f"Output file {out_csv} was not created."

    # Generate expected output using the canonical Go implementation
    canonical_go = """package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

func readFloats(filename string) []float64 {
	content, _ := os.ReadFile(filename)
	lines := strings.Split(strings.TrimSpace(string(content)), "\\n")
	var floats []float64
	for _, line := range lines {
		f, _ := strconv.ParseFloat(line, 64)
		floats = append(floats, f)
	}
	return floats
}

func getDist(data []float64) []float64 {
	dist := make([]float64, 10)
	for _, v := range data {
		idx := int(v * 10.0)
		if idx >= 10 {
			idx = 9
		}
		if idx < 0 {
			idx = 0
		}
		dist[idx]++
	}
	for i := range dist {
		dist[i] /= float64(len(data))
	}
	return dist
}

func main() {
	ref := readFloats("/home/user/reference.txt")
	samp := readFloats("/home/user/sample.txt")

	rng := rand.New(rand.NewSource(42))
	rng.Shuffle(len(samp), func(i, j int) {
		samp[i], samp[j] = samp[j], samp[i]
	})

	refDist := getDist(ref)

	fmt.Println("N,TVD")
	for n := 100; n <= 1000; n += 100 {
		subSamp := samp[:n]
		subDist := getDist(subSamp)

		tvd := 0.0
		for i := 0; i < 10; i++ {
			tvd += math.Abs(refDist[i] - subDist[i])
		}
		tvd *= 0.5

		fmt.Printf("%d,%.6f\\n", n, tvd)
	}
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        go_file = os.path.join(tmpdir, "canonical.go")
        with open(go_file, "w") as f:
            f.write(canonical_go)

        # Run the canonical Go code
        comp = subprocess.run(['go', 'run', go_file], capture_output=True, text=True)
        assert comp.returncode == 0, "Failed to run canonical Go code for truth generation."
        expected_output = comp.stdout.strip()

    with open(out_csv, 'r') as f:
        student_output = f.read().strip()

    assert student_output == expected_output, f"Contents of {out_csv} do not match the expected output.\nExpected:\n{expected_output}\n\nGot:\n{student_output}"