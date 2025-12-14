import torch
import cv2 as cv
import numpy as np
import pathlib

# Configuracion requerida para windows
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

model = torch.hub.load('ultralytics/yolov5', 'custom', force_reload=True,
                       path='') # TODO:Manejar esto en variables de entorno


cap = cv.imread('../../resources/pistolas/glock.jpg')

while True:
    # Realizamos deteccion
    detect = model(cap)

    # Muestra la imagen en una ventana
    cv.imshow('Detector de pistolas', np.squeeze(detect.render()))

    # Espera a que el usuario toque una tecla
    cv.waitKey(0)
    break

cv.destroyAllWindows()


def detectar_pistola(ruta_imagen):
    model = torch.hub.load(
        'ultralytics/yolov5',
        'custom',
        force_reload=True,
        path=ruta_imagen)

    # Realizamos deteccion
    detect = model(cap)


    # Muestra la imagen en una ventana
    cv.imshow('Detector de pistolas', np.squeeze(detect.render()))
