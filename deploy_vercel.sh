#!/bin/bash

echo "🚀 Deploy Automático - Lugar Imóveis"
echo "======================================"
echo ""

# Verificar se o Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo "📦 Instalando Vercel CLI..."
    npm i -g vercel
fi

echo "✅ Vercel CLI instalado"
echo ""

# Fazer build
echo "🔨 Criando build de produção..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build criado com sucesso"
    echo ""

    # Deploy
    echo "🚀 Fazendo deploy no Vercel..."
    cd dist
    vercel --prod

    echo ""
    echo "======================================"
    echo "✅ Deploy concluído!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Copie a URL gerada acima"
    echo "2. Atualize streamlit_app/app_new.py com sua URL"
    echo "3. Faça deploy no Streamlit Cloud"
    echo ""
    echo "💡 Ou use apenas a URL do Vercel diretamente!"
    echo "======================================"
else
    echo "❌ Erro no build. Verifique os logs acima."
    exit 1
fi
