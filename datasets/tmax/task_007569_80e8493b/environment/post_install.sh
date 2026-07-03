apt-get update && apt-get install -y python3 python3-pip git bash
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/repo
    cd /home/user/repo
    git init

    git config --global user.email "dev@example.com"
    git config --global user.name "Developer"

    # Base script (Good)
    cat << 'EOF' > calc_convergence.sh
#!/bin/bash
x=$1
if [ -z "$x" ]; then echo "Provide a number"; exit 1; fi
guess=1
prev_guess=0
while [ "$guess" -ne "$prev_guess" ]; do
    prev_guess=$guess
    guess=$(( (guess + x / guess) / 2 ))
done
echo $guess
EOF
    chmod +x calc_convergence.sh

    git add calc_convergence.sh
    git commit -m "Initial commit with working convergence script"
    git tag v1.0

    # Create 100 good commits
    for i in $(seq 1 100); do
        echo "dummy $i" > "dummy_$i.txt"
        git add "dummy_$i.txt"
        git commit -m "Add dummy file $i"
    done

    # Create the BAD commit (Commit 101)
    cat << 'EOF' > calc_convergence.sh
#!/bin/bash
# Added some comments
# SECRET_KEY="B59x-L92Q-PZ11-M00X"
x=$1
if [ -z "$x" ]; then echo "Provide a number"; exit 1; fi
guess=1
prev_guess=0
while [ "$guess" -ne "$prev_guess" ]; do
    prev_guess=$((guess - 1)) 
    guess=$(( (guess + x / guess) / 2 ))
done
echo $guess
EOF
    git add calc_convergence.sh
    git commit -m "Refactor convergence update logic"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Create Commit 102 (Remove secret)
    sed -i '/SECRET_KEY/d' calc_convergence.sh
    git add calc_convergence.sh
    git commit -m "Remove accidentally committed secret key"

    # Create remaining commits up to 200
    for i in $(seq 102 200); do
        echo "dummy $i" > "dummy_$i.txt"
        git add "dummy_$i.txt"
        git commit -m "Add dummy file $i"
    done

    # Save the expected bad commit for verification
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chown -R user:user /home/user/repo
    chmod -R 777 /home/user