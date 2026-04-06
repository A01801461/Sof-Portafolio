import os
import shutil
from PIL import Image

# Configuración
ASSETS_DIR = "./assets"
OUTPUT_STD_DIR = "./assets/img/std"
OUTPUT_HIGH_DIR = "./assets/img/high"

QUALITY_STD = 80
QUALITY_HIGH = 92
# Carpetas originales a ignorar internamente
# Ej. si se requiere en el futuro
IGNORE_DIRS = ['assets\\img', 'assets/img']

def process_and_convert_to_webp(directory):
    for root, dirs, files in os.walk(directory):
        # Ignorar si estamos dentro la carpeta de output previamente creada
        if 'img/std' in root.replace('\\', '/') or 'img/high' in root.replace('\\', '/'):
            continue
            
        for file in files:
            # Solo procesar imágenes que NO sean ya webp
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(root, file)
                
                # Obtener la ruta relativa respecto a ./assets para espejar la estructura
                rel_path = os.path.relpath(root, ASSETS_DIR)
                if rel_path == '.':
                    rel_path = ''
                
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
                        width, height = img.size
                        
                        # Guardar High-Res (Original size, High Quality)
                        img.save(high_filepath, "WEBP", quality=QUALITY_HIGH, optimize=True)
                        
                        # Generar Std-Res
                        if is_a_choice:
                            # Según las reglas, A Choice no se reduce la resolución
                            resized_img = img
                        else:
                            # 1/4 area (width/2, height/2)
                            new_size = (width // 2, height // 2)
                            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                        
                        # Guardar Std-Res (Low Quality/Balanced)
                        resized_img.save(std_filepath, "WEBP", quality=QUALITY_STD, optimize=True)
                        
                    # Borrar el archivo original
                    os.remove(filepath)
                    print(f"✨ Procesado: {file} -> std/high (.webp)")
                        
                except Exception as e:
                    print(f"❌ Error con {file}: {e}")

if __name__ == "__main__":
    print("🚀 Optimizando portafolio de Sofía Abud (Doble Resolución WebP)...")
    process_and_convert_to_webp(ASSETS_DIR)
    print("✅ ¡Proceso terminado! Imágenes establescidad en assets/img/...")