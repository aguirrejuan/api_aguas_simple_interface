import os 
import re


def get_image(path_image):
    name_image_with_extension = os.path.basename(path_image)
    name_image, extension = os.path.splitext(name_image_with_extension)
    extension = extension.lower().replace('.', '')  # Normalize extension to lowercase without the dot
    return [
        ('image', (
            name_image_with_extension,  # Include the extension in the filename
            open(path_image, 'rb'),
            f'image/{extension}'  # Correct MIME type
        ))
    ]


def get_image_paths(folder):
    files_ = os.listdir(folder)

    path_images = []

    for name_file in files_:
        ruta_imagen = os.path.join(folder, name_file)
        if name_file.endswith((".jpg", ".jpeg", ".png")):
            path_images.append(ruta_imagen)

    return path_images