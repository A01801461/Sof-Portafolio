import os
import shutil
from PIL import Image

# Configuración
ASSETS_DIR = "./assets"
OUTPUT_STD_DIR = "./assets/img/std"
OUTPUT_HIGH_DIR = "./assets/img/high"

# Calidad según requerimientos (85 para std, 100 para high)
QUALITY_STD = 85
QUALITY_HIGH = 100

# Carpetas originales a ignorar internamente
IGNORE_DIRS = ['assets\\img', 'assets/img']

def process_and_convert_to_webp(directory):
    for root, dirs, files in os.walk(directory):
        # Ignorar si estamos dentro la carpeta de output previamente creada
        root_normalized = root.replace('\\', '/')
        if 'img/std' in root_normalized or 'img/high' in root_normalized:
            continue
            
        for file in files:
            # Solo procesar imágenes que NO sean ya webp
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(root, file)
                
                # Obtener la ruta relativa respecto a ./assets para espejar la estructura
                rel_path = os.path.relpath(root, ASSETS_DIR)
                if rel_path == '.':
                    rel_path = ''
                
                # Mapeos de carpetas de entrada a carpetas de salida en img/
                rel_parts = rel_path.split(os.sep)
                if len(rel_parts) > 0:
                    if rel_parts[0] == 'unprocessed':
                        # unprocessed/ -> photography/
                        rel_parts[0] = 'photography'
                    elif rel_parts[0] == 'AC':
                        # AC/ -> cinematography/AC/
                        if 'cinematography' not in rel_parts:
                            rel_parts.insert(0, 'cinematography')
                
                rel_path = os.path.join(*rel_parts)
                
                # Crear los directorios destino
                std_dest_dir = os.path.join(OUTPUT_STD_DIR, rel_path)
                high_dest_dir = os.path.join(OUTPUT_HIGH_DIR, rel_path)
                
                os.makedirs(std_dest_dir, exist_ok=True)
                os.makedirs(high_dest_dir, exist_ok=True)
                
                base_name = os.path.splitext(file)[0]
                std_filepath = os.path.join(std_dest_dir, base_name + ".webp")
                high_filepath = os.path.join(high_dest_dir, base_name + ".webp")
                
                try:
                    with Image.open(filepath) as img:
                        # Convertir a RGB por si acaso
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                            
                        width, height = img.size
                        is_horizontal = width > height
                        
                        # Definir tamaños objetivos según tipo de proyecto
                        if 'cinematography' in rel_parts:
                            # Estándares Cinematográficos (FM, UIFY, AC)
                            target_high = (4096, 2160) if is_horizontal else (2160, 4096)
                            target_std = (2048, 1080) if is_horizontal else (1080, 2048)
                        else:
                            # Estándares Fotográficos (Photography)
                            target_high = (2850, 1911) if is_horizontal else (1911, 2850)
                            target_std = (955, 425) if is_horizontal else (425, 955)
                        
                        # Generar y guardar High-Res (Quality 100)
                        # thumbnail() mantiene el tamaño si la imagen es más pequeña que el target
                        high_img = img.copy()
                        high_img.thumbnail(target_high, Image.Resampling.LANCZOS)
                        high_img.save(high_filepath, "WEBP", quality=QUALITY_HIGH, lossless=True if QUALITY_HIGH==100 else False, optimize=True)
                        
                        # Generar y guardar Std-Res (Quality 85)
                        std_img = img.copy()
                        std_img.thumbnail(target_std, Image.Resampling.LANCZOS)
                        std_img.save(std_filepath, "WEBP", quality=QUALITY_STD, optimize=True)
                        
                    # Borrar el archivo original
                    os.remove(filepath)
                    print(f"Processed: {file} -> std/high (.webp) in {rel_path}")
                        
                except Exception as e:
                    print(f"Error with {file}: {e}")

    # Al finalizar, borramos la carpeta AC si existe y esta vacía
    # (El script ya borró los archivos individuales arriba)
    ac_dir = os.path.join(ASSETS_DIR, 'AC')
    if os.path.exists(ac_dir):
        try:
            if not os.listdir(ac_dir): # Solo si está vacía
                os.rmdir(ac_dir)
                print(f"Temporal folder {ac_dir} deleted.")
        except Exception as e:
            print(f"Could not delete folder {ac_dir}: {e}")

if __name__ == "__main__":
    print("Optimizing portfolio - Sofía Abud (Cinematography Standards)...")
    process_and_convert_to_webp(ASSETS_DIR)
    print("Process finished! Images located in assets/img/...")