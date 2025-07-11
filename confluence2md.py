#!/usr/bin/env python3
"""
Script para convertir archivos .doc de Confluence a markdown.
Recorre recursivamente una carpeta buscando archivos .doc y los convierte a .md
"""

import os
import sys
import re
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import html2text
import quopri
import html


def extract_html_from_confluence_doc(file_path, show_decoded=False):
    """
    Extrae el contenido HTML de un archivo .doc de Confluence.
    Elimina la cabecera MIME y extrae solo el contenido HTML.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Buscar el contenido HTML después de la cabecera MIME
        html_pattern = r'<html[^>]*>.*?</html>'
        html_match = re.search(html_pattern, content, re.DOTALL | re.IGNORECASE)
        
        if html_match:
            html_content = html_match.group(0)
            # Decodificar caracteres especiales
            html_content = decode_special_characters(html_content, show_decoded)
            return html_content
        else:
            print(f"Error: No se encontró contenido HTML en {file_path}")
            return None
            
    except Exception as e:
        print(f"Error al leer el archivo {file_path}: {e}")
        return None


def decode_special_characters(content, show_decoded=False):
    """
    Decodifica caracteres especiales codificados en quoted-printable y HTML entities.
    """
    if not content:
        return content
    
    decoded_chars = []
    
    # Decodificar quoted-printable
    try:
        content = quopri.decodestring(content).decode('utf-8', errors='ignore')
    except:
        pass
    
    # Decodificar HTML entities
    try:
        content = html.unescape(content)
    except:
        pass
    
    # Mapeo específico de caracteres comunes de Confluence
    character_mapping = {
        '=E2=80=A6': '…',  # Puntos suspensivos
        '=E2=80=9D': '"',  # Comilla doble derecha
        '=E2=80=9C': '"',  # Comilla doble izquierda
        '=E2=80=99': ''',  # Comilla simple derecha
        '=E2=80=98': ''',  # Comilla simple izquierda
        '=E2=80=93': '–',  # Guión corto
        '=E2=80=94': '—',  # Guión largo
        '=C2=A0': ' ',     # Espacio no separador
        '=E2=80=8B': '',   # Espacio de ancho cero
        '=E2=80=8C': '',   # Espacio de ancho cero
        '=E2=80=8D': '',   # Espacio de ancho cero
        '=E2=80=8E': '',   # Espacio de ancho cero
        '=E2=80=8F': '',   # Espacio de ancho cero
        '=E2=80=9A': ',',  # Coma baja
        '=E2=80=9E': '"',  # Comilla doble baja
        '=E2=80=B2': '²',  # Superíndice 2
        '=E2=80=B3': '³',  # Superíndice 3
        '=E2=80=B9': '‹',  # Comilla simple angular izquierda
        '=E2=80=BA': '›',  # Comilla simple angular derecha
        '=E2=81=84': '⁄',  # Barra de fracción
        '=E2=81=85': '⁅',  # Corchete izquierdo con raya
        '=E2=81=86': '⁆',  # Corchete derecho con raya
        '=E2=81=87': '⁇',  # Signo de interrogación doble
        '=E2=81=88': '⁈',  # Signo de interrogación y exclamación
        '=E2=81=89': '⁉',  # Signo de exclamación e interrogación
        '=E2=81=8A': '⁊',  # Tironian et
        '=E2=81=8B': '⁋',  # Reversed pilcrow sign
        '=E2=81=8C': '⁌',  # Black leftwards bullet
        '=E2=81=8D': '⁍',  # Black rightwards bullet
        '=E2=81=8E': '⁎',  # Low asterisk
        '=E2=81=8F': '⁏',  # Reversed semicolon
        '=E2=81=90': '⁐',  # Close up
        '=E2=81=91': '⁑',  # Two asterisks aligned vertically
        '=E2=81=92': '⁒',  # Commercial minus sign
        '=E2=81=93': '⁓',  # Swung dash
        '=E2=81=94': '⁔',  # Inverted undertie
        '=E2=81=95': '⁕',  # Flower punctuation mark
        '=E2=81=96': '⁖',  # Three dot punctuation
        '=E2=81=97': '⁗',  # Four dot punctuation
        '=E2=81=98': '⁘',  # Four dot mark
        '=E2=81=99': '⁙',  # Five dot mark
        '=E2=81=9A': '⁚',  # Two dot punctuation
        '=E2=81=9B': '⁛',  # Four dot mark
        '=E2=81=9C': '⁜',  # Dotted cross
        '=E2=81=9D': '⁝',  # Four dot mark
        '=E2=81=9E': '⁞',  # Five dot mark
    }
    
    # Aplicar mapeo de caracteres y registrar los encontrados
    for encoded, decoded in character_mapping.items():
        if encoded in content:
            count = content.count(encoded)
            if show_decoded:
                decoded_chars.append(f"  {encoded} → {decoded} ({count} veces)")
            content = content.replace(encoded, decoded)
    
    # Mostrar información sobre caracteres decodificados
    if show_decoded and decoded_chars:
        print("Caracteres especiales decodificados:")
        for char_info in decoded_chars:
            print(char_info)
        print()
    
    # Limpiar caracteres de control y espacios extra
    content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
    
    return content


def html_to_markdown(html_content, preserve_spacing=False):
    """
    Convierte contenido HTML a markdown usando html2text.
    """
    try:
        # Configurar html2text para una mejor conversión
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0  # Sin límite de ancho
        h.unicode_snob = True
        h.escape_snob = True
        h.single_line_break = True  # Usar un solo salto de línea
        h.emphasis = True
        h.strong_emphasis = True
        h.code_tag_on = True
        h.ul_item_mark = '-'  # Usar guión para listas no numeradas
        h.list_indent = '  '  # Indentación para listas
        
        markdown_content = h.handle(html_content)
        
        # Post-procesar para mejorar listas y tablas
        markdown_content = post_process_markdown(markdown_content)
        
        # Mejorar formato de tablas
        markdown_content = improve_table_formatting(markdown_content)
        
        # Limpiar saltos de línea múltiples solo si no se preserva el espaciado
        if not preserve_spacing:
            markdown_content = clean_markdown_content(markdown_content)
        
        return markdown_content
        
    except Exception as e:
        print(f"Error al convertir HTML a markdown: {e}")
        return None


def post_process_markdown(content):
    """
    Post-procesa el markdown para mejorar listas y tablas.
    """
    if not content:
        return content
    
    lines = content.split('\n')
    processed_lines = []
    in_list = False
    in_table = False
    list_level = 0
    
    for i, line in enumerate(lines):
        current_line = line.rstrip()
        
        # Detectar si estamos en una tabla
        if is_table_row(current_line):
            if not in_table:
                in_table = True
                # Agregar línea vacía antes de la tabla
                if processed_lines and processed_lines[-1] != '':
                    processed_lines.append('')
            processed_lines.append(current_line)
            continue
        elif in_table and not current_line.strip():
            # Fin de tabla
            in_table = False
            processed_lines.append('')
            continue
        elif in_table:
            processed_lines.append(current_line)
            continue
        
        # Procesar listas
        stripped_line = current_line.strip()
        
        # Detectar elementos de lista
        is_list_item = False
        list_marker = None
        
        # Detectar listas no numeradas
        if stripped_line.startswith(('* ', '- ', '+ ')):
            is_list_item = True
            list_marker = stripped_line[:2]
            list_content = stripped_line[2:].strip()
        # Detectar listas numeradas
        elif re.match(r'^\d+\.\s', stripped_line):
            is_list_item = True
            list_marker = re.match(r'^\d+\.\s', stripped_line).group(0)
            list_content = stripped_line[len(list_marker):].strip()
        # Detectar elementos de lista con indentación
        elif current_line.startswith('  ') and stripped_line.startswith(('* ', '- ', '+ ')):
            is_list_item = True
            list_marker = stripped_line[:2]
            list_content = stripped_line[2:].strip()
        
        if is_list_item:
            if not in_list:
                # Agregar línea vacía antes de la lista
                if processed_lines and processed_lines[-1] != '':
                    processed_lines.append('')
                in_list = True
            
            # Asegurar que use guión (-) para listas no numeradas
            if list_marker in ['* ', '+ ']:
                processed_lines.append(f'- {list_content}')
            else:
                processed_lines.append(current_line)
            continue
        elif in_list and not current_line.strip():
            # Línea vacía dentro de la lista
            processed_lines.append('')
            continue
        elif in_list and not is_list_item:
            # Fin de lista
            in_list = False
            processed_lines.append('')
            processed_lines.append(current_line)
            continue
        
        # Líneas normales
        processed_lines.append(current_line)
    
    return '\n'.join(processed_lines)


def is_table_row(line):
    """
    Detecta si una línea es parte de una tabla.
    """
    if not line.strip():
        return False
    
    # Verificar si contiene barras verticales y tiene contenido en las celdas
    if '|' not in line:
        return False
    
    cells = line.split('|')
    # Debe tener al menos 3 partes (inicio vacío, contenido, fin vacío)
    if len(cells) < 3:
        return False
    
    # Verificar que hay contenido en las celdas del medio
    content_cells = [cell.strip() for cell in cells[1:-1]]
    return any(cell for cell in content_cells)


def improve_table_formatting(content):
    """
    Mejora el formato de las tablas en markdown.
    """
    if not content:
        return content
    
    lines = content.split('\n')
    improved_lines = []
    in_table = False
    table_lines = []
    
    for line in lines:
        if is_table_row(line):
            if not in_table:
                in_table = True
                # Agregar línea vacía antes de la tabla
                if improved_lines and improved_lines[-1] != '':
                    improved_lines.append('')
            table_lines.append(line)
        elif in_table:
            # Procesar tabla completa
            if table_lines:
                improved_table = format_table(table_lines)
                improved_lines.extend(improved_table)
                improved_lines.append('')
            in_table = False
            table_lines = []
            improved_lines.append(line)
        else:
            improved_lines.append(line)
    
    # Procesar tabla final si existe
    if in_table and table_lines:
        improved_table = format_table(table_lines)
        improved_lines.extend(improved_table)
    
    return '\n'.join(improved_lines)


def format_table(table_lines):
    """
    Formatea una tabla para que sea válida en markdown.
    """
    if not table_lines:
        return []
    
    # Encontrar el número máximo de columnas
    max_columns = 0
    for line in table_lines:
        columns = len(line.split('|')) - 2  # Restar las barras del inicio y fin
        max_columns = max(max_columns, columns)
    
    if max_columns == 0:
        return table_lines
    
    # Procesar cada línea de la tabla
    formatted_lines = []
    header_separator_added = False
    
    for line in table_lines:
        cells = line.split('|')
        # Limpiar celdas vacías del inicio y fin
        cells = [cell.strip() for cell in cells[1:-1]]
        
        # Rellenar con celdas vacías si es necesario
        while len(cells) < max_columns:
            cells.append('')
        
        # Crear línea formateada
        formatted_line = '| ' + ' | '.join(cells) + ' |'
        formatted_lines.append(formatted_line)
        
        # Agregar separador de encabezado después de la primera línea
        if not header_separator_added:
            separator = '|' + '|'.join(['---'] * max_columns) + '|'
            formatted_lines.append(separator)
            header_separator_added = True
    
    return formatted_lines


def clean_markdown_content(content):
    """
    Limpia el contenido markdown para evitar saltos de línea múltiples innecesarios.
    """
    if not content:
        return content
    
    # Normalizar saltos de línea
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Eliminar múltiples saltos de línea consecutivos (más de 2)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Eliminar espacios en blanco al final de las líneas
    content = re.sub(r'[ \t]+\n', '\n', content)
    
    # Eliminar líneas vacías al principio y final
    content = content.strip()
    
    # Procesar línea por línea para un mejor control
    lines = content.split('\n')
    cleaned_lines = []
    in_code_block = False
    in_list = False
    
    for i, line in enumerate(lines):
        current_line = line.rstrip()  # Mantener espacios al inicio para indentación
        
        # Detectar bloques de código
        if current_line.startswith('```') or current_line.startswith('    '):
            if not in_code_block:
                in_code_block = True
            cleaned_lines.append(current_line)
            continue
        elif in_code_block:
            cleaned_lines.append(current_line)
            if current_line.startswith('```'):
                in_code_block = False
            continue
        
        # Detectar listas (ya procesadas por post_process_markdown)
        is_list_item = (current_line.strip().startswith(('* ', '- ', '+ ')) or 
                       re.match(r'^\d+\.\s', current_line.strip()))
        
        if is_list_item:
            if not in_list:
                # Agregar línea vacía antes de la lista si no hay una
                if cleaned_lines and cleaned_lines[-1] != '':
                    cleaned_lines.append('')
            in_list = True
            cleaned_lines.append(current_line)
            continue
        elif in_list and not current_line.strip():
            # Mantener línea vacía después de listas
            cleaned_lines.append('')
            in_list = False
            continue
        elif in_list:
            # Continuar lista (elementos con indentación)
            if current_line.strip():
                cleaned_lines.append(current_line)
            continue
        
        # Detectar encabezados
        if current_line.strip().startswith('#'):
            # Agregar línea vacía antes del encabezado si no hay una
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
            cleaned_lines.append(current_line)
            continue
        
        # Para líneas normales
        if current_line.strip():
            cleaned_lines.append(current_line)
        elif i > 0 and lines[i-1].strip():
            # Solo agregar línea vacía si la anterior no está vacía
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
    
    # Eliminar líneas vacías al final
    while cleaned_lines and cleaned_lines[-1] == '':
        cleaned_lines.pop()
    
    return '\n'.join(cleaned_lines)


def process_file(file_path, preserve_spacing=False, show_decoded=False):
    """
    Procesa un archivo .doc de Confluence y crea su versión en markdown.
    """
    try:
        # Extraer HTML del archivo
        html_content = extract_html_from_confluence_doc(file_path, show_decoded)
        if not html_content:
            return False
        
        # Convertir HTML a markdown
        markdown_content = html_to_markdown(html_content, preserve_spacing)
        if not markdown_content:
            return False
        
        # Crear el archivo markdown con el mismo nombre pero extensión .md
        output_path = str(file_path).replace('.doc', '.md')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✓ Convertido: {file_path} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"Error procesando {file_path}: {e}")
        return False


def find_doc_files(directory):
    """
    Encuentra todos los archivos .doc en el directorio y subdirectorios.
    """
    doc_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.doc'):
                doc_files.append(os.path.join(root, file))
    return doc_files


def main():
    parser = argparse.ArgumentParser(
        description='Convierte archivos .doc de Confluence a markdown'
    )
    parser.add_argument(
        'directory',
        help='Directorio a procesar (por defecto: directorio actual)',
        nargs='?',
        default='.'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada'
    )
    parser.add_argument(
        '--preserve-spacing',
        action='store_true',
        help='Preservar espaciado original (menos limpieza de saltos de línea)'
    )
    parser.add_argument(
        '--show-decoded',
        action='store_true',
        help='Mostrar información sobre caracteres decodificados'
    )
    
    args = parser.parse_args()
    
    # Verificar que el directorio existe
    if not os.path.exists(args.directory):
        print(f"Error: El directorio '{args.directory}' no existe.")
        sys.exit(1)
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' no es un directorio.")
        sys.exit(1)
    
    print(f"Buscando archivos .doc en: {os.path.abspath(args.directory)}")
    
    # Encontrar archivos .doc
    doc_files = find_doc_files(args.directory)
    
    if not doc_files:
        print("No se encontraron archivos .doc en el directorio especificado.")
        return
    
    print(f"Encontrados {len(doc_files)} archivos .doc")
    
    # Procesar cada archivo
    successful_conversions = 0
    failed_conversions = 0
    
    for doc_file in doc_files:
        if args.verbose:
            print(f"Procesando: {doc_file}")
        
        if process_file(doc_file, args.preserve_spacing, args.show_decoded):
            successful_conversions += 1
        else:
            failed_conversions += 1
    
    # Resumen final
    print(f"\nResumen:")
    print(f"  ✓ Conversiones exitosas: {successful_conversions}")
    print(f"  ✗ Conversiones fallidas: {failed_conversions}")
    print(f"  Total archivos procesados: {len(doc_files)}")


if __name__ == "__main__":
    main() 