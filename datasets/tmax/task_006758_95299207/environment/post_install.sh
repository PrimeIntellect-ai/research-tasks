apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    mkdir -p /home/user/math_parser
    cd /home/user/math_parser
    git init

    cat << 'EOF' > calc.sh
#!/bin/bash
op=$1
a=$2
b=$3
if [[ ! "$a" =~ ^-?[0-9]+$ ]] || [[ ! "$b" =~ ^-?[0-9]+$ ]]; then
    echo "Error"
    exit 1
fi
case $op in
    ADD) echo $(($a + $b)) ;;
    SUB) echo $(($a - $b)) ;;
    MUL) echo $(($a * $b)) ;;
    DIV) echo $(($a / $b)) ;;
    *) echo "Error" ; exit 1 ;;
esac
EOF
    chmod +x calc.sh
    git add calc.sh
    git commit -m "Initial commit"
    git tag v1.0

    for i in $(seq 1 149); do
        echo "# comment $i" >> calc.sh
        git commit -am "Commit $i"
    done

    # Commit 150: introduce bug (breaks negative numbers for second argument)
    sed -i 's/\[\[ ! "$b" =\~ \^-?\[0-9\]+\$ \]\]/[[ ! "$b" =~ ^[0-9]+$ ]]/' calc.sh
    git commit -am "Optimize regex parsing"
    BUG_COMMIT=$(git rev-parse HEAD)

    for i in $(seq 151 201); do
        echo "# comment $i" >> calc.sh
        git commit -am "Commit $i"
    done

    echo "$BUG_COMMIT" > /tmp/expected_bug_commit.txt

    chown -R user:user /home/user/math_parser
    chmod -R 777 /home/user