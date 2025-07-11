#!/bin/bash

# Script de instalación para confluence2md
# Convierte archivos .doc de Confluence a markdown

set -e

echo "=== Instalador de confluence2md ==="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "confluence2md.py" ]; then
    echo "Error: No se encontró confluence2md.py en el directorio actual."
    echo "Ejecuta este script desde el directorio del proyecto."
    exit 1
fi

# Verificar que Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado."
    echo "Por favor, instala Python3 antes de continuar."
    exit 1
fi

# Verificar que pip está instalado
if ! command -v pip &> /dev/null; then
    echo "Error: pip no está instalado."
    echo "Por favor, instala pip antes de continuar."
    exit 1
fi

echo "✓ Python3 y pip están instalados"
echo ""

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
pip install pyinstaller

echo "✓ Dependencias instaladas"
echo ""

# Compilar con PyInstaller
echo "Compilando con PyInstaller..."
pyinstaller confluence2md.spec

if [ ! -f "dist/confluence2md" ]; then
    echo "Error: La compilación falló."
    exit 1
fi

echo "✓ Compilación completada"
echo ""

# Instalar en /usr/local/bin
echo "Instalando en /usr/local/bin..."
sudo cp dist/confluence2md /usr/local/bin/
sudo chmod +x /usr/local/bin/confluence2md

echo "✓ Instalación completada"
echo ""

# Verificar la instalación
if command -v confluence2md &> /dev/null; then
    echo "✓ confluence2md está instalado correctamente"
    echo ""
    echo "Uso:"
    echo "  confluence2md [directorio]     # Procesar directorio (por defecto: actual)"
    echo "  confluence2md --help           # Mostrar ayuda"
    echo "  confluence2md --verbose        # Modo verbose"
    echo ""
    echo "Ejemplo:"
    echo "  confluence2md /path/to/docs    # Convertir todos los .doc en /path/to/docs"
else
    echo "✗ Error: confluence2md no se instaló correctamente"
    exit 1
fi 