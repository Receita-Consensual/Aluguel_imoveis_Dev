#!/bin/bash

echo "═══════════════════════════════════════════════════════════════"
echo "🚀 PREPARANDO PARA DEPLOY NO STREAMLIT CLOUD"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Verificar arquivos essenciais
echo "✅ Verificando arquivos..."
FILES=(
    "app.py"
    "app_debug.py"
    "requirements.txt"
    ".streamlit/config.toml"
)

ALL_OK=true
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file encontrado"
    else
        echo "   ❌ $file NÃO encontrado!"
        ALL_OK=false
    fi
done

echo ""

if [ "$ALL_OK" = true ]; then
    echo "🎉 TUDO PRONTO PARA DEPLOY!"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "📋 PRÓXIMOS PASSOS:"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "1. Subir para GitHub:"
    echo "   git add ."
    echo "   git commit -m 'App pronto para deploy'"
    echo "   git push origin main"
    echo ""
    echo "2. Abrir Streamlit Cloud:"
    echo "   https://share.streamlit.io/"
    echo ""
    echo "3. Criar novo app:"
    echo "   - Clique em 'Create app'"
    echo "   - Selecione seu repositório"
    echo "   - Branch: main"
    echo "   - Main file: app.py"
    echo "   - Clique 'Deploy!'"
    echo ""
    echo "4. Aguardar 2-3 minutos"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "📖 Mais detalhes em: DEPLOY_AGORA.txt"
    echo "═══════════════════════════════════════════════════════════════"
else
    echo "❌ ERRO: Alguns arquivos essenciais não foram encontrados!"
    echo "Por favor, certifique-se que todos os arquivos estão presentes."
fi
