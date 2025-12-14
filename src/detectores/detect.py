import torch
import cv2 as cv
import numpy as np
import platform
import pathlib

# Configuración de rutas según el sistema operativo
# Solo aplicar el fix de Windows si estamos en Windows
if platform.system() == 'Windows':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath


def detectar_pistola(ruta_imagen):
    """
    Detecta objetos en una imagen usando YOLOv5.

    Args:
        ruta_imagen: Ruta a la imagen a analizar

    Returns:
        Resultados de la detección
    """
    if not ruta_imagen:
        print("No se seleccionó ninguna imagen")
        return None

    # Cargar el modelo YOLOv5 preentrenado
    # Nota: Para detección específica de pistolas, necesitarías un modelo entrenado
    # Por ahora usamos yolov5s que detecta objetos generales
    model = torch.hub.load(
        'ultralytics/yolov5',
        'yolov5s',  # Modelo preentrenado base
        pretrained=True
    )

    # Leer la imagen
    imagen = cv.imread(ruta_imagen)

    if imagen is None:
        print(f"Error: No se pudo cargar la imagen: {ruta_imagen}")
        return None

    # Realizar detección
    detect = model(imagen)

    # Imprimir resultados en consola
    print(detect)

    # Mostrar la imagen con las detecciones en una ventana
    cv.imshow('Detector - PySentinel', np.squeeze(detect.render()))

    # Esperar a que el usuario presione una tecla
    cv.waitKey(0)
    cv.destroyAllWindows()

    return detect


# Solo ejecutar si se llama directamente este archivo
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
    else:
        ruta = input("Ingresa la ruta de la imagen: ")

    detectar_pistola(ruta)
