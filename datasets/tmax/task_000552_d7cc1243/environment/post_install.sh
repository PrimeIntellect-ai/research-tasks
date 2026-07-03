apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

# Install C++ toolchain and DB client libraries
apt-get install -y g++ make libpq-dev libhiredis-dev postgresql-client redis-tools

# Create directories
mkdir -p /home/user/reference
mkdir -p /home/user/workspace

# Create reference files
cat << 'EOF' > /home/user/reference/users.csv
user_id,name,account_status
101,Alice,VERIFIED
102,Bob,PENDING
103,Charlie,VERIFIED
EOF

cat << 'EOF' > /home/user/reference/products.csv
product_id,category,is_active
501,Electronics,true
502,Books,false
503,Clothing,true
EOF

cat << 'EOF' > /home/user/reference/load_redis.sh
#!/bin/bash
redis-cli SET txn_999 1
redis-cli SET txn_666 1
EOF
chmod +x /home/user/reference/load_redis.sh

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user