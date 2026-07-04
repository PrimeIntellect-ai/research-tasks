apt-get update && apt-get install -y python3 python3-pip golang upx-ucl binutils
    pip3 install pytest

    # Create app directory
    mkdir -p /app
    cat << 'EOF' > /app/sec_eval.go
package main
import "fmt"
func main() {
    fmt.Println("0.0")
}
EOF
    cd /app
    go build -o sec_eval sec_eval.go
    strip -s sec_eval
    upx sec_eval || true
    chmod +x sec_eval

    # Create user
    useradd -m -s /bin/bash user || true

    # Create app_code directories and files
    mkdir -p /home/user/app_code/static
    mkdir -p /home/user/app_code/templates

    echo "console.log('hello');" > /home/user/app_code/static/app.js
    echo "<html><body><script>console.log('inline');</script></body></html>" > /home/user/app_code/templates/index.html

    echo "db_pass=admin" > /home/user/app_code/config.ini
    echo "#!/bin/bash\necho 'running'" > /home/user/app_code/helper.sh

    # Set permissions
    chmod -R 777 /home/user

    # Explicitly set required permissions after the recursive chmod to preserve SUID
    chmod 4755 /home/user/app_code/helper.sh
    chmod 777 /home/user/app_code/config.ini