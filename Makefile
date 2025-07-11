# Makefile para confluence2md
# Script para convertir archivos .doc de Confluence a markdown

.PHONY: help install-deps build install clean uninstall test

# Variables
SCRIPT_NAME = confluence2md
INSTALL_DIR = /usr/local/bin
BUILD_DIR = dist
SPEC_FILE = $(SCRIPT_NAME).spec

help:
	@echo "Makefile para confluence2md"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  install-deps  - Instalar dependencias de Python"
	@echo "  build         - Compilar el script con PyInstaller"
	@echo "  install       - Instalar el ejecutable en $(INSTALL_DIR)"
	@echo "  clean         - Limpiar archivos de compilación"
	@echo "  uninstall     - Desinstalar el ejecutable"
	@echo "  test          - Ejecutar el script en modo de prueba"
	@echo "  all           - Ejecutar install-deps, build e install"

all: install-deps build install

install-deps:
	@echo "Instalando dependencias..."
	pip install -r requirements.txt
	pip install pyinstaller

build: install-deps
	@echo "Compilando con PyInstaller..."
	pyinstaller $(SPEC_FILE)
	@echo "Compilación completada. Ejecutable creado en $(BUILD_DIR)/$(SCRIPT_NAME)"

install: build
	@echo "Instalando en $(INSTALL_DIR)..."
	@if [ ! -d "$(INSTALL_DIR)" ]; then \
		echo "Creando directorio $(INSTALL_DIR)..."; \
		sudo mkdir -p $(INSTALL_DIR); \
	fi
	sudo cp $(BUILD_DIR)/$(SCRIPT_NAME) $(INSTALL_DIR)/
	sudo chmod +x $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "Instalación completada. Ejecuta '$(SCRIPT_NAME) --help' para ver las opciones."

clean:
	@echo "Limpiando archivos de compilación..."
	rm -rf build/
	rm -rf dist/
	rm -f *.spec
	@echo "Limpieza completada."

uninstall:
	@echo "Desinstalando $(SCRIPT_NAME)..."
	sudo rm -f $(INSTALL_DIR)/$(SCRIPT_NAME)
	@echo "Desinstalación completada."

test:
	@echo "Ejecutando script en modo de prueba..."
	python3 $(SCRIPT_NAME).py --help

# Verificar si el script está instalado
check-install:
	@if command -v $(SCRIPT_NAME) >/dev/null 2>&1; then \
		echo "✓ $(SCRIPT_NAME) está instalado en $(shell which $(SCRIPT_NAME))"; \
	else \
		echo "✗ $(SCRIPT_NAME) no está instalado"; \
	fi

# Mostrar información del sistema
info:
	@echo "Información del sistema:"
	@echo "  Python: $(shell python3 --version)"
	@echo "  Pip: $(shell pip --version)"
	@echo "  Directorio de instalación: $(INSTALL_DIR)"
	@echo "  Script: $(SCRIPT_NAME).py" 