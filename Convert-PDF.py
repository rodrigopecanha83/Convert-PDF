import os
import sys
from pathlib import Path
from PIL import Image
import img2pdf
import shutil

# Ativar o prg através do menu de contexto no NEMO.
# Colocar o script.sh na pasta:
# diretorio="/home/rodrigo/.local/share/nemo/scripts"

def convert_image_to_pdf(image_path, output_pdf):
    try:
        # Converte a imagem para PDF
        with open(output_pdf, "wb") as f:
            f.write(img2pdf.convert(image_path))
        print(f"Convertido: {image_path} -> {output_pdf}")
    except Exception as e:
        print(f"Erro ao converter {image_path} para PDF: {e}")

def normalize_extensions(directory):
    """Converte as extensões de todos os arquivos para minúsculas no diretório especificado."""
    for file in Path(directory).iterdir():
        if file.is_file():
            new_file = file.with_suffix(file.suffix.lower())
            if file != new_file:
                try:
                    file.rename(new_file)
                    print(f"Renomeado: {file} -> {new_file}")
                except Exception as e:
                    print(f"Erro ao renomear {file}: {e}")

def move_original_to_trash(image_file, trash_dir):
    """Move o arquivo original para a pasta de lixo."""
    try:
        trash_dir.mkdir(exist_ok=True)  # Cria a pasta de lixo, se não existir
        shutil.move(str(image_file), str(trash_dir / image_file.name))
        print(f"Movido para o lixo: {image_file} -> {trash_dir / image_file.name}")
    except Exception as e:
        print(f"Erro ao mover {image_file} para o lixo: {e}")

def convert_images_in_directory(directory):
    # Formatos de imagem suportados
    supported_formats = ('.jpg', '.jpeg', '.png', '.heic', '.webp', '.avif')
    
    directory_path = Path(directory)
    if not directory_path.exists():
        print(f"Diretório {directory} não existe.")
        return

    # Normaliza as extensões
    normalize_extensions(directory)

    # Cria a pasta de lixo
    trash_dir = directory_path / "Lixo-Conversão-PDF"

    # Lista os arquivos suportados no diretório
    image_files = [file for file in directory_path.iterdir() if file.suffix.lower() in supported_formats]
    
    if not image_files:
        print("Nenhuma imagem encontrada para conversão.")
        return

    # Processa cada imagem
    for image_file in image_files:
        try:
            # Testa se a imagem pode ser aberta pelo PIL
            with Image.open(image_file) as img:
                img.verify()  # Verifica se a imagem está intacta

            # Define o nome do arquivo PDF
            output_pdf = image_file.with_suffix(".pdf")
            convert_image_to_pdf(str(image_file), str(output_pdf))
            
            # Move a imagem original para a pasta de lixo
            move_original_to_trash(image_file, trash_dir)
        except Exception as e:
            print(f"Erro ao processar a imagem {image_file}: {e}")

if __name__ == "__main__":
    # Obtém o diretório alvo (passado como argumento ou usa o diretório atual)
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        target_directory = os.getcwd()

    convert_images_in_directory(target_directory)
