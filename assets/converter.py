import os
import shutil
from PIL import Image

# Configuración
ASSETS_DIR = "./assets"
OUTPUT_STD_DIR = "./assets/img/std"
OUTPUT_HIGH_DIR = "./assets/img/high"

QUALITY_STD = 85
QUALITY_HIGH = 95
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
                
                # Si viene de unprocessed, lo mapeamos a photography
                rel_parts = rel_path.split(os.sep)
                if len(rel_parts) > 0 and rel_parts[0] == 'unprocessed':
                    # remove 'unprocessed' and prepend 'photography'
                    rel_parts[0] = 'photography'
                    rel_path = os.path.join(*rel_parts)
                
                # Excepciones
                # "2M" folder ignorado en caso de video, pero si hay imagen (poster) se procede.
                is_a_choice = 'AC' in rel_path.split(os.sep)
                
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
                        
                        # Tamaños máximos dependiendo de la orientación
                        high_size = (2850, 1911) if is_horizontal else (1911, 2850)
                        std_size = (955, 425) if is_horizontal else (425, 955)
                        
                        # Generar y guardar High-Res
                        high_img = img.copy()
                        high_img.thumbnail(high_size, Image.Resampling.LANCZOS)
                        high_img.save(high_filepath, "WEBP", quality=QUALITY_HIGH, optimize=True)
                        
                        # Generar y guardar Std-Res
                        std_img = img.copy()
                        if is_a_choice:
                            # Según las reglas previas, A Choice no se reduce la resolución (aunque lo generamos igual)
                            pass
                        else:
                            # thumbnail no agranda la imagen si ya es más pequeña que std_size
                            std_img.thumbnail(std_size, Image.Resampling.LANCZOS)
                            
                        std_img.save(std_filepath, "WEBP", quality=QUALITY_STD, optimize=True)
                        
                    # Borrar el archivo original
                    os.remove(filepath)
                    print(f"✨ Procesado: {file} -> std/high (.webp) en {rel_path}")
                        
                except Exception as e:
                    print(f"❌ Error con {file}: {e}")

    # Al finalizar, borramos la carpeta unprocessed si existe y esta vacía o solo contiene subcarpetas vacías
    unprocessed_dir = os.path.join(ASSETS_DIR, 'unprocessed')
    if os.path.exists(unprocessed_dir):
        try:
            shutil.rmtree(unprocessed_dir)
            print(f"🗑️ Carpeta original {unprocessed_dir} eliminada.")
        except Exception as e:
            print(f"❌ No se pudo eliminar la carpeta {unprocessed_dir}: {e}")

if __name__ == "__main__":
    print("🚀 Optimizando portafolio de Sofía Abud (Doble Resolución WebP)...")
    process_and_convert_to_webp(ASSETS_DIR)
    print("✅ ¡Proceso terminado! Imágenes establescidad en assets/img/...")