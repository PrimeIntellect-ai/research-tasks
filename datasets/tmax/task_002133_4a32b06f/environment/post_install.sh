apt-get update && apt-get install -y python3 python3-pip git gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/metrics_build
    cd /home/user/metrics_build
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    cat << 'EOF' > measurements.csv
id,value
1,0.111111111
2,0.222222222
3,0.333333333
EOF

    cat << 'EOF' > compute_mean.sh
#!/bin/bash
awk -F, 'NR>1 {sum+=$2; count++} END {print sum/count}' measurements.csv
EOF
    chmod +x compute_mean.sh

    cat << 'EOF' > publish.sh
#!/bin/bash
API_TOKEN="SEC-8f7a9b2d4c"
echo "Publishing with token $API_TOKEN"
EOF
    chmod +x publish.sh

    git add measurements.csv compute_mean.sh publish.sh
    git commit -m "Initial commit with analytics scripts"

    cat << 'EOF' > publish.sh
#!/bin/bash
API_TOKEN=$ENV_API_TOKEN
echo "Publishing with token $API_TOKEN"
EOF

    git add publish.sh
    git commit -m "Security: Remove hardcoded API token"

    cat << 'EOF' > test_build.sh
#!/bin/bash

# Check Token
if [ ! -f /home/user/recovered_token.txt ]; then
    echo "FAIL: Token file missing"
    exit 1
fi

TOKEN=$(cat /home/user/recovered_token.txt | tr -d ' \n')
if [ "$TOKEN" != "SEC-8f7a9b2d4c" ]; then
    echo "FAIL: Incorrect token recovered"
    exit 1
fi

# Check Precision
MEAN=$(bash /home/user/metrics_build/compute_mean.sh)
if [ "$MEAN" != "0.222222222" ]; then
    echo "FAIL: Precision test failed. Got: $MEAN"
    exit 1
fi

echo "BUILD OK" > /home/user/build_success.log
echo "Success!"
EOF
    chmod +x test_build.sh

    chown -R user:user /home/user/metrics_build
    chmod -R 777 /home/user