apt-get update && apt-get install -y python3 python3-pip cargo
    pip3 install pytest

    mkdir -p /app/text-dedup-engine/src

    cat << 'EOF' > /app/text-dedup-engine/Cargo.toml
[package]
name = "text-dedup-engine"
version = "0.1.0"
edition = "2099"
EOF

    cat << 'EOF' > /app/text-dedup-engine/src/lib.rs
pub fn compute_hash(input: &str) -> u64 {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    let mut hasher = DefaultHasher::new();
    input.hash(&mut hasher);
    hasher.finish()
}
EOF

    cat << 'EOF' > /tmp/generate_data.py
import random, string
random.seed(42)
words = ["data", "science", "rust", "normalization", "hashing", "duplicate", "pipeline", "agent", "task"]
raw_lines = []
gold_lines = set()
for _ in range(5000):
    line_words = random.choices(words, k=random.randint(3, 8))
    gold_str = " ".join(line_words)
    gold_lines.add(gold_str)

    noisy_words = line_words.copy()
    if random.random() > 0.5:
        noisy_words = [w.capitalize() for w in noisy_words]
    noisy_str = "  ".join(noisy_words) + random.choice(string.punctuation)
    raw_lines.append(noisy_str)

    if random.random() > 0.7:
        raw_lines.append(noisy_str + " ")

with open('/home/user/raw_corpus.txt', 'w') as f:
    f.write('\n'.join(raw_lines))
with open('/tmp/golden_corpus.txt', 'w') as f:
    f.write('\n'.join(gold_lines))
EOF

    cat << 'EOF' > /tmp/eval.py
import sys
def load_set(path):
    with open(path, 'r') as f:
        return set(line.strip() for line in f if line.strip())
pred = load_set('/home/user/clean_corpus.txt')
gold = load_set('/tmp/golden_corpus.txt')
tp = len(pred & gold)
fp = len(pred - gold)
fn = len(gold - pred)
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
print(f"{f1:.4f}")
EOF

    useradd -m -s /bin/bash user || true
    python3 /tmp/generate_data.py

    chmod -R 777 /home/user
    chmod -R 777 /app