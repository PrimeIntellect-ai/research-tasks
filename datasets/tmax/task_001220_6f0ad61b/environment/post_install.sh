apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    # 1. Create fragmented logs
    mkdir -p /home/user/logs
    cat << 'EOF' > /home/user/logs/worker_1.log
[10:01:23] INFO: Received optimization request job_id=8831
[10:01:24] DEBUG: Points batch 1 parsed: (0.0, 0.0), (0.0, 4.0)
EOF

    cat << 'EOF' > /home/user/logs/worker_2.log
[10:01:25] DEBUG: Points batch 2 parsed: (3.0, 0.0)
[10:01:25] INFO: Initializing guess at bounds min: (0.0, 0.0)
[10:01:26] ERROR: job_id=8831 failed with ZeroDivisionError in Weiszfeld iteration.
EOF

    # 2. Create the git repository
    mkdir -p /home/user/weiszfeld_solver
    cd /home/user/weiszfeld_solver
    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"

    cat << 'EOF' > solver.py
import math

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def weiszfeld_step(points, guess, epsilon=1e-8):
    x_num, y_num, den = 0.0, 0.0, 0.0
    for p in points:
        dist = distance(p, guess)
        weight = 1.0 / (dist + epsilon)
        x_num += p[0] * weight
        y_num += p[1] * weight
        den += weight
    return (x_num / den, y_num / den)

def solve(points, initial_guess, iterations=100):
    current = initial_guess
    for _ in range(iterations):
        current = weiszfeld_step(points, current)
    return current

if __name__ == "__main__":
    # Example usage
    pts = [(0,0), (0,4), (3,0)]
    print(solve(pts, (1,1)))
EOF

    git add solver.py
    git commit -m "Initial commit: basic Weiszfeld solver with epsilon"

    # Create 143 good commits
    for i in $(seq 1 143); do
        echo "# comment $i" >> solver.py
        git commit -am "Minor update $i"
    done

    # Create the BAD commit (remove epsilon)
    cat << 'EOF' > solver.py
import math

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def weiszfeld_step(points, guess):
    x_num, y_num, den = 0.0, 0.0, 0.0
    for p in points:
        dist = distance(p, guess)
        weight = 1.0 / dist
        x_num += p[0] * weight
        y_num += p[1] * weight
        den += weight
    return (x_num / den, y_num / den)

def solve(points, initial_guess, iterations=100):
    current = initial_guess
    for _ in range(iterations):
        current = weiszfeld_step(points, current)
    return current

if __name__ == "__main__":
    # Example usage
    pts = [(0,0), (0,4), (3,0)]
    print(solve(pts, (1,1)))
EOF
    git commit -am "Optimize: remove epsilon for exact distance calculation"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Create 56 more commits
    for i in $(seq 145 200); do
        echo "# comment $i" >> solver.py
        git commit -am "Minor update $i"
    done

    # Save the expected bad commit for verification invisibly
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/logs /home/user/weiszfeld_solver
    chmod -R 777 /home/user