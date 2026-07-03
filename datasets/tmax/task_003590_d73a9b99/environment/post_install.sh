apt-get update && apt-get install -y python3 python3-pip ffmpeg cargo
    pip3 install pytest

    # Generate dummy video file
    mkdir -p /app
    ffmpeg -f lavfi -i testsrc=duration=5:size=320x240:rate=30 -c:v libx264 -pix_fmt yuv420p /app/scene.mp4

    # Build oracle binary
    mkdir -p /opt/oracle && cd /opt/oracle
    cargo new graph_projector_oracle
    cd graph_projector_oracle
    cat << 'EOF' > src/main.rs
use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet};

fn main() {
    let stdin = io::stdin();
    let mut adj: HashMap<u32, HashSet<u32>> = HashMap::new();
    let mut all_nodes = HashSet::new();

    for line in stdin.lock().lines() {
        if let Ok(l) = line {
            let parts: Vec<&str> = l.split(',').collect();
            if parts.len() >= 3 {
                if let (Ok(u), Ok(v), Ok(w)) = (parts[0].parse::<u32>(), parts[1].parse::<u32>(), parts[2].parse::<f64>()) {
                    all_nodes.insert(u);
                    all_nodes.insert(v);
                    if w > 0.5 {
                        adj.entry(u).or_insert_with(HashSet::new).insert(v);
                        adj.entry(v).or_insert_with(HashSet::new).insert(u);
                    }
                }
            }
        }
    }

    let mut visited = HashSet::new();
    let mut components = Vec::new();

    for &node in &all_nodes {
        if !visited.contains(&node) {
            let mut comp = Vec::new();
            let mut stack = vec![node];
            visited.insert(node);

            while let Some(curr) = stack.pop() {
                comp.push(curr);
                if let Some(neighbors) = adj.get(&curr) {
                    for &neighbor in neighbors {
                        if !visited.contains(&neighbor) {
                            visited.insert(neighbor);
                            stack.push(neighbor);
                        }
                    }
                }
            }
            comp.sort_unstable();
            components.push(comp);
        }
    }

    components.sort_by(|a, b| {
        b.len().cmp(&a.len()).then_with(|| a[0].cmp(&b[0]))
    });

    let json = serde_json::to_string(&components).unwrap();
    println!("{}", json);
}
EOF
    cargo add serde_json
    cargo build --release
    cp target/release/graph_projector_oracle /opt/oracle/graph_projector

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user