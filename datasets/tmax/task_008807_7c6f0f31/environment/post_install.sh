apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create the user
    useradd -m -s /bin/bash user || true

    # Create directories
    mkdir -p /home/user/build_system/src \
             /home/user/build_system/lib \
             /home/user/build_system/traces \
             /home/user/build_system/out

    # Create modules.list
    cat << 'EOF' > /home/user/build_system/modules.list
auth_service
payment_gateway
inventory_manager
notification_worker
api_router
EOF

    # Create module files
    for mod in auth_service payment_gateway inventory_manager notification_worker api_router; do
        mkdir -p "/home/user/build_system/src/$mod"
        echo "config for $mod" > "/home/user/build_system/src/$mod/config"
        echo "INFO: Starting $mod" > "/home/user/build_system/traces/${mod}.log"
        echo "DEBUG: Initializing memory" >> "/home/user/build_system/traces/${mod}.log"
        echo "INFO: $mod loaded" >> "/home/user/build_system/traces/${mod}.log"
    done

    # Create build.sh
    cat << 'EOF' > /home/user/build_system/build.sh
#!/bin/bash
cd /home/user/build_system
source lib/utils.sh

rm -rf out/*
mkdir -p out

echo "Starting build process..."

while read -r module; do
    [[ -z "$module" || "$module" == \#* ]] && continue
    echo "Processing $module..."
    build_module "$module"
done < modules.list

echo "Packaging release..."
tar -czf out/release.tar.gz -C out .
echo "Build complete."
EOF
    chmod +x /home/user/build_system/build.sh

    # Create utils.sh
    cat << 'EOF' > /home/user/build_system/lib/utils.sh
build_module() {
    local mod=$1
    mkdir -p "out/$mod"

    # Simulate compilation
    cp "src/$mod/config" "out/$mod/config.bin"

    # Process module trace logs
    format_logs "$mod" "traces/${mod}.log"

    touch "out/$mod/done"
}

format_logs() {
    local mod=$1
    local logfile=$2

    # BUG: cat without arguments reads from stdin.
    # Because this function is called inside a `while read` loop that redirects from `modules.list`,
    # `cat` will consume the rest of `modules.list` as its standard input.
    cat | grep -v "DEBUG" > "out/$mod/filtered.log"
}
EOF
    chmod +x /home/user/build_system/lib/utils.sh

    # Fix permissions
    chmod -R 777 /home/user