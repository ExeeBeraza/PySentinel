import sys
import torch
import cv2 as cv
import numpy as np
import platform
import pathlib

# Agregar el directorio src al path para imports
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from config.config import MODEL_PATH

# Configuración de rutas según el sistema operativo
# Solo aplicar el fix de Windows si estamos en Windows
if platform.system() == 'Windows':
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath


def detectar_pistola(ruta_imagen, mostrar_ventana=False):
    """
    Detecta objetos en una imagen usando YOLOv5.

    Args:
        ruta_imagen: Ruta a la imagen a analizar
        mostrar_ventana: Si True, muestra la imagen con OpenCV (default: False)

    Returns:
        Resultados de la detección (objeto YOLO Results)
    """
    if not ruta_imagen:
        print("No se seleccionó ninguna imagen")
        return None

    # Cargar el modelo YOLOv5 preentrenado
    # Nota: Para detección específica de pistolas, necesitarías un modelo entrenado
    model = torch.hub.load(
        'ultralytics/yolov5',
        'custom',
        path=MODEL_PATH
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

    # Mostrar la imagen con las detecciones en una ventana (opcional)
    if mostrar_ventana:
        cv.imshow('Detector - PySentinel', np.squeeze(detect.render()))
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

    # Al ejecutar directamente, mostrar ventana
    detectar_pistola(ruta, mostrar_ventana=True)

