#!/bin/bash

echo "========================================="
echo "VERIFICACAO DE STATUS - LUGAR"
echo "========================================="
echo ""

# Verificar processos
echo "1. PROCESSOS:"
if ps aux | grep -E "python3.*http.server" | grep -v grep > /dev/null; then
    echo "   ✓ Servidor HTTP rodando"
else
    echo "   ✗ Servidor HTTP NAO esta rodando"
fi

if ps aux | grep -E "ssh.*serveo" | grep -v grep > /dev/null; then
    echo "   ✓ Tunel Serveo ativo"
else
    echo "   ✗ Tunel Serveo NAO esta ativo"
fi

echo ""
echo "2. SERVIDOR LOCAL:"
if curl -s -I http://localhost:8080 | head -1 | grep "200" > /dev/null; then
    echo "   ✓ Respondendo em http://localhost:8080"
else
    echo "   ✗ NAO esta respondendo"
fi

echo ""
echo "3. URL PUBLICA:"
URL=$(grep -o "https://[a-z0-9\-]*\.serveousercontent\.com" /tmp/serveo.log 2>/dev/null | tail -1)
if [ -z "$URL" ]; then
    echo "   ✗ Nenhuma URL encontrada"
else
    echo "   URL: $URL"
    if curl -s -I "$URL" | head -1 | grep "200" > /dev/null; then
        echo "   ✓ URL publica funcionando"
    else
        echo "   ✗ URL publica NAO responde"
    fi
fi

echo ""
echo "========================================="
