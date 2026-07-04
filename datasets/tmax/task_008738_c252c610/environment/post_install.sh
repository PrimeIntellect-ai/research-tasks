apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/markov_solver
cd /home/user/markov_solver
git init

export GIT_AUTHOR_NAME="Dev"
export GIT_AUTHOR_EMAIL="dev@example.com"
export GIT_COMMITTER_NAME="Dev"
export GIT_COMMITTER_EMAIL="dev@example.com"

cat << 'EOF' > solver.py
def solve_steady_state(transition_matrix, iterations=50):
    n = len(transition_matrix)
    state = [1.0 / n] * n
    for it in range(iterations):
        next_state = [0.0] * n
        for i in range(n):
            for j in range(n):
                next_state[i] += state[j] * transition_matrix[j][i]
        state = next_state
    return state
EOF

cat << 'EOF' > test_solver.py
from solver import solve_steady_state
matrix = [
    [0.1, 0.9],
    [0.5, 0.5]
]
state = solve_steady_state(matrix, iterations=20)
assert abs(sum(state) - 1.0) < 1e-5, f"State sum is {sum(state)}"
print("OK")
EOF

export GIT_AUTHOR_DATE="2023-01-01T12:00:00"
export GIT_COMMITTER_DATE="2023-01-01T12:00:00"
git add solver.py test_solver.py
git commit -m "Initial commit"
git tag v1.0

for i in 2 3 4 5; do
    export GIT_AUTHOR_DATE="2023-01-0${i}T12:00:00"
    export GIT_COMMITTER_DATE="2023-01-0${i}T12:00:00"
    echo "# comment $i" >> solver.py
    git commit -am "Minor update $i"
done

export GIT_AUTHOR_DATE="2023-01-06T12:00:00"
export GIT_COMMITTER_DATE="2023-01-06T12:00:00"
cat << 'EOF' > solver.py
def solve_steady_state(transition_matrix, iterations=50):
    n = len(transition_matrix)
    state = [1.0 / n] * n
    for it in range(iterations):
        next_state = [0.0] * n
        for i in range(n):
            for j in range(n):
                # Bug introduced here: subtracting a small epsilon decays the probability mass
                next_state[i] += state[j] * (transition_matrix[j][i] - 0.006)
        state = next_state
    return state
EOF
echo "# comment 5" >> solver.py
git commit -am "Optimize inner loop calculation"

for i in 7 8 9 10; do
    if [ "$i" = "10" ]; then
        export GIT_AUTHOR_DATE="2023-01-10T12:00:00"
        export GIT_COMMITTER_DATE="2023-01-10T12:00:00"
    else
        export GIT_AUTHOR_DATE="2023-01-0${i}T12:00:00"
        export GIT_COMMITTER_DATE="2023-01-0${i}T12:00:00"
    fi
    echo "# comment $i" >> test_solver.py
    git commit -am "Update tests $i"
done

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user