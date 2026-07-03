apt-get update && apt-get install -y python3 python3-pip gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/generate_data.sh
#!/bin/bash
awk -v seed=$1 'BEGIN{
  srand(seed);
  for(i=1;i<=1000;i++){
    for(j=1;j<=10;j++){
      printf "%.2f%s", rand()*100, (j==10?"":",")
    }
    print ""
  }
}' > /home/user/data_$1.csv
EOF
    chmod +x /home/user/generate_data.sh

    chmod -R 777 /home/user