# test_final_state.py

import os
import shutil
import subprocess
import pytest

def test_result_exists():
    path = "/home/user/result.txt"
    assert os.path.exists(path), f"Missing {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_main_rs_fixed():
    path = "/home/user/gc_bootstrap/src/main.rs"
    assert os.path.exists(path), f"Missing {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "sample.par_iter().sum()" not in content, "The non-deterministic parallel reduction `sample.par_iter().sum()` is still present in main.rs"

def test_correct_output(tmp_path):
    # We dynamically compile and run the known-fixed Rust code to get the exact expected output
    # This avoids hardcoding brittle floating-point results that might depend on the Rust/Cargo version.

    src_dir = "/home/user/gc_bootstrap"
    dst_dir = tmp_path / "gc_bootstrap"
    shutil.copytree(src_dir, dst_dir)

    truth_main_rs = """use rand::{SeedableRng, Rng};
use rand_chacha::ChaCha8Rng;
use rayon::prelude::*;
use std::fs;

fn main() {
    let fasta = fs::read_to_string("/home/user/sequences.fasta").expect("Unable to read fasta");
    let mut gc_contents: Vec<f64> = Vec::new();

    for line in fasta.lines() {
        if !line.starts_with('>') && !line.is_empty() {
            let gc = line.chars().filter(|&c| c == 'G' || c == 'C').count() as f64;
            gc_contents.push(gc / line.len() as f64);
        }
    }

    let mut rng = ChaCha8Rng::seed_from_u64(42);
    let mut bootstrap_means = Vec::new();

    let n = gc_contents.len();
    for _ in 0..1000 {
        let sample: Vec<f64> = (0..n).map(|_| {
            let idx = rng.gen_range(0..n);
            gc_contents[idx]
        }).collect();

        // Fixed: Sequential reduction
        let sum: f64 = sample.iter().sum();
        bootstrap_means.push(sum / n as f64);
    }

    let overall_mean: f64 = bootstrap_means.iter().sum::<f64>() / bootstrap_means.len() as f64;
    println!("{:.10}", overall_mean);
}
"""
    main_rs_path = dst_dir / "src" / "main.rs"
    with open(main_rs_path, "w") as f:
        f.write(truth_main_rs)

    result = subprocess.run(
        ["cargo", "run", "--release", "--manifest-path", str(dst_dir / "Cargo.toml")],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to compile and run the truth Rust code"

    expected_output = result.stdout.strip()

    with open("/home/user/result.txt", "r") as f:
        student_output = f.read().strip()

    assert student_output == expected_output, f"Incorrect value in result.txt. Expected '{expected_output}', got '{student_output}'"