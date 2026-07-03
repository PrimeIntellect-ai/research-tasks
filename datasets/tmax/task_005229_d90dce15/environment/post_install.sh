apt-get update && apt-get install -y python3 python3-pip git jq bc coreutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/repo
    cd /home/user/repo
    git init

    git config user.name "Dev"
    git config user.email "dev@example.com"

    # Create base script
    cat << 'EOF' > simulate.sh
#!/bin/bash
CONFIG=$(cat config.b64 | sed 's/\r//g' | base64 -d)
RATE=$(echo "$CONFIG" | jq -r .rate)
VAL=1.0
for i in {1..10}; do
    VAL=$(echo "$VAL + $RATE" | bc -l)
done
echo "Converged to $VAL"
EOF
    chmod +x simulate.sh

    # Create base64 encoded config containing the letter 'r' when encoded
    echo "eyJyYXRlIjogMC41LCAicGFkZGluZyI6ICJ0aGlzIGlzIHNvbWUgcGFkZGluZyB0byBlbnN1cmUgYW4gciBhcHBlYXJzIn0K" > config.b64

    git add simulate.sh config.b64
    GIT_AUTHOR_DATE="2020-01-01T00:00:00" GIT_COMMITTER_DATE="2020-01-01T00:00:00" git commit -m "Initial commit"
    git tag v1.0

    # Create 100 good commits
    for i in {1..100}; do
        echo "# Good comment $i" >> simulate.sh
        GIT_AUTHOR_DATE="2020-01-01T00:01:$i" GIT_COMMITTER_DATE="2020-01-01T00:01:$i" git commit -am "Minor update $i"
    done

    # Introduce the bug in commit 101
    sed -i 's/s\/\\r\/\/g/s\/r\/\/g/' simulate.sh
    GIT_AUTHOR_DATE="2020-01-01T00:05:00" GIT_COMMITTER_DATE="2020-01-01T00:05:00" git commit -am "Refactor config reading to fix line endings"
    BAD_HASH=$(git rev-parse HEAD)

    # Create 99 more commits
    for i in {1..99}; do
        echo "# Another comment $i" >> simulate.sh
        GIT_AUTHOR_DATE="2020-01-01T00:10:$i" GIT_COMMITTER_DATE="2020-01-01T00:10:$i" git commit -am "More updates $i"
    done

    # Write the bad hash to a hidden file for verification purposes
    echo "$BAD_HASH" > /tmp/true_bad_commit.txt

    chown -R user:user /home/user/repo
    chmod -R 777 /home/user