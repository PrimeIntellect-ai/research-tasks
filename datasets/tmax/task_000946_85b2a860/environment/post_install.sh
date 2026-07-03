apt-get update && apt-get install -y python3 python3-pip dos2unix gawk
    pip3 install pytest

    mkdir -p /app/corpus/clean /app/corpus/evil

    cat << 'EOF' > /app/corpus/clean/translations1.csv
Key,Source,Target
ui.welcome,Welcome {user} to the {app}!,Bienvenue {user} dans l'{app}!
ui.button.save,Save,Enregistrer
ui.items,You have {count} items.,Vous avez {count} articles.
EOF

    cat << 'EOF' > /app/corpus/evil/malicious1.csv
Key,Source,Target
ui.error,Error {code}: {msg},Erreur {cde}: {msg}
ui.xss,Hello {name},Bonjour {name} <ScRiPt>alert(1)</script>
ui.link,Click here,Cliquez <a href="javascript:void(0)">ici</a>
ui.mismatch,Value {val},Valeur {value}
EOF

    cat << 'EOF' > /app/i18n_compiler
#!/bin/bash
# Mock compiler
echo "Compiling $1 to $2"
EOF
    chmod +x /app/i18n_compiler

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user