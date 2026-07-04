apt-get update && apt-get install -y python3 python3-pip git gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'OUTER' > /tmp/setup.sh
#!/bin/bash

mkdir -p /home/user/data_pipeline
cd /home/user/data_pipeline

git config --global init.defaultBranch master
git config --global user.email "test@example.com"
git config --global user.name "Test User"

git init

cat << 'EOF' > input.csv
id,category,value
1,ALPHA,10
2,BETA,15
3,ALPHA,20
4,GAMMA,5
5,BETA,25
6,DELTA,30
7,ALPHA,5
8,DELTA,10
EOF

git add input.csv

for i in {1..200}; do
    cat << 'EOF' > transform.sh
#!/bin/bash
# Simple aggregator
awk -F, 'NR>1 {sum[$2]+=$3} END {for (k in sum) print k, sum[k]}' input.csv | sort
EOF

    if [ "$i" -ge 142 ]; then
        cat << 'EOF' > transform.sh
#!/bin/bash
# Simple aggregator with an intermittent bug
awk -F, -v seed=$RANDOM 'NR>1 {sum[$2]+=$3} END {for (k in sum) { if (k == "BETA" && seed % 4 == 0) continue; print k, sum[k]}}' input.csv | sort
EOF
    fi

    echo "# Revision $i" >> transform.sh

    chmod +x transform.sh
    git add transform.sh

    export GIT_COMMITTER_DATE="2024-01-01 12:00:$(printf "%02d" $((i % 60)))"
    export GIT_AUTHOR_DATE="2024-01-01 12:00:$(printf "%02d" $((i % 60)))"

    git commit -m "Update transform script: Revision $i" > /dev/null
done

git log --grep="Revision 142" --format="%H" > /tmp/expected_bad_commit.txt
OUTER

    bash /tmp/setup.sh
    rm /tmp/setup.sh

    chmod -R 777 /home/user
    chmod 777 /tmp/expected_bad_commit.txt