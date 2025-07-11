# confluence2md

Script en Python que recorre de forma recursiva una carpeta buscando archivos `.doc` de Confluence y los convierte a `.md` (markdown). Es decir, crea un archivo con el mismo nombre en la misma ubicación pero con la extensión `.md` con la versión en markdown del archivo de origen.

## Descripción

Los archivos "word" de Confluence tienen un formato especial de Word. Tienen una cabecera del tipo:

```
Date: Fri, 1 Jun  ... (UTC)
Message-ID: <...>
Subject: Exported From Confluence
MIME-Version: 1.0
Content-Type: multipart/related; 
	boundary="----=_Part_8_.."

------=_Part_8_...
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: quoted-printable
Content-Location: file:///C:/exported.html

<html xmlns:o=3D'urn:schemas-microsoft-com:office:office'
      xmlns:w=3D'urn:schemas-microsoft-com:office:word'
      xmlns:v=3D'urn:schemas-microsoft-com:vml'
      xmlns=3D'urn:w3-org-ns:HTML'>
<head>
 [...]
</head>
</html>
```

El script elimina la cabecera MIME y extrae solo el contenido HTML para luego convertirlo a markdown.

## Instalación

### Opción 1: Instalación automática (recomendada)

```bash
# Clonar o descargar el proyecto
git clone <url-del-repositorio>
cd confluence2md

# Ejecutar el instalador automático
./install.sh
```

### Opción 2: Instalación manual con Makefile

```bash
# Instalar dependencias, compilar e instalar
make all

# O paso a paso:
make install-deps    # Instalar dependencias
make build          # Compilar con PyInstaller
make install        # Instalar en /usr/local/bin
```

### Opción 3: Instalación manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt
pip install pyinstaller

# 2. Compilar con PyInstaller
pyinstaller confluence2md.spec

# 3. Instalar el ejecutable
sudo cp dist/confluence2md /usr/local/bin/
sudo chmod +x /usr/local/bin/confluence2md
```

## Uso

### Comando básico

```bash
# Procesar el directorio actual
confluence2md

# Procesar un directorio específico
confluence2md /path/to/docs

# Modo verbose (más información)
confluence2md --verbose /path/to/docs
```

### Opciones disponibles

- `[directorio]`: Directorio a procesar (por defecto: directorio actual)
- `--verbose, -v`: Mostrar información detallada del proceso
- `--preserve-spacing`: Preservar espaciado original (menos limpieza de saltos de línea)
- `--show-decoded`: Mostrar información sobre caracteres especiales decodificados
- `--help`: Mostrar ayuda

### Ejemplos

```bash
# Convertir todos los archivos .doc en el directorio actual
confluence2md

# Convertir archivos .doc en una carpeta específica
confluence2md /home/user/documents/confluence-exports

# Ver información detallada del proceso
confluence2md --verbose /home/user/documents/confluence-exports

# Preservar espaciado original (menos limpieza de saltos de línea)
confluence2md --preserve-spacing /home/user/documents/confluence-exports

# Mostrar caracteres especiales decodificados
confluence2md --show-decoded /home/user/documents/confluence-exports
```

## Funcionalidades

- ✅ Recorre recursivamente directorios buscando archivos `.doc`
- ✅ Extrae contenido HTML de archivos de Confluence
- ✅ Convierte HTML a markdown usando `html2text`
- ✅ Preserva enlaces e imágenes
- ✅ Limpieza inteligente de saltos de línea múltiples
- ✅ Conversión mejorada de listas (usando guiones `-`)
- ✅ Formato mejorado de tablas con separadores automáticos
- ✅ Decodificación automática de caracteres especiales (quoted-printable)
- ✅ Preservación de formato en listas, encabezados y bloques de código
- ✅ Opción para preservar espaciado original
- ✅ Opción para mostrar caracteres decodificados
- ✅ Manejo de errores robusto
- ✅ Modo verbose para debugging
- ✅ Resumen de conversiones al final

## Estructura del proyecto

```
confluence2md/
├── confluence2md.py      # Script principal
├── requirements.txt      # Dependencias de Python
├── confluence2md.spec   # Configuración de PyInstaller
├── Makefile            # Automatización de instalación
├── install.sh          # Script de instalación automática
└── README.md           # Este archivo
```

## Comandos del Makefile

```bash
make help              # Mostrar ayuda
make install-deps      # Instalar dependencias
make build             # Compilar con PyInstaller
make install           # Instalar el ejecutable
make clean             # Limpiar archivos de compilación
make uninstall         # Desinstalar el ejecutable
make test              # Ejecutar script en modo prueba
make all               # Ejecutar install-deps, build e install
make check-install     # Verificar si está instalado
make info              # Mostrar información del sistema
```

## Desinstalación

```bash
# Usando Makefile
make uninstall

# Manualmente
sudo rm -f /usr/local/bin/confluence2md
```

## Dependencias

- Python 3.6+
- beautifulsoup4
- html2text
- lxml
- pyinstaller (para compilación)

## Caracteres especiales

El script decodifica automáticamente caracteres especiales codificados en formato `quoted-printable` que aparecen comúnmente en archivos de Confluence:

### Caracteres más comunes:
- `=E2=80=A6` → `…` (puntos suspensivos)
- `=E2=80=9D` → `"` (comilla doble derecha)
- `=E2=80=9C` → `"` (comilla doble izquierda)
- `=E2=80=99` → `'` (comilla simple derecha)
- `=E2=80=98` → `'` (comilla simple izquierda)
- `=E2=80=93` → `–` (guión corto)
- `=E2=80=94` → `—` (guión largo)

### Ver caracteres decodificados:
```bash
confluence2md --show-decoded /path/to/docs
```

## Solución de problemas

### Error: "No se encontró contenido HTML"
- Verifica que el archivo `.doc` sea realmente un archivo exportado de Confluence
- Asegúrate de que el archivo no esté corrupto

### Error: "Permission denied"
- Ejecuta el comando con `sudo` para la instalación
- Verifica que tengas permisos de escritura en `/usr/local/bin`

### Error: "Python3 no está instalado"
- Instala Python 3 desde [python.org](https://python.org)
- En Ubuntu/Debian: `sudo apt install python3 python3-pip`

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 


