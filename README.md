# PySentinel - Sistema de Detección de Armas

Sistema para la detección y clasificación de armas utilizando técnicas de visión computacional con YOLOv5 y OpenCV.

## 📋 Requisitos del Sistema

- **Python**: 3.10 o superior
- **Sistema Operativo**: macOS, Linux o Windows
- **Espacio en disco**: ~2GB (para dependencias y modelos)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd PySentinel
```

### 2. Crear entorno virtual

```bash
python3 -m venv yolov5env
```

### 3. Activar el entorno virtual

**macOS/Linux:**
```bash
source yolov5env/bin/activate
```

**Windows:**
```bash
yolov5env\Scripts\activate
```

### 4. Instalar Tkinter (dependencia del sistema)

Tkinter es la librería gráfica que usa la aplicación. La instalación varía según tu sistema operativo:

**Windows:**
> ✅ Tkinter viene incluido con la instalación estándar de Python. No necesitas instalar nada adicional.

**macOS (con Homebrew):**
```bash
# Verifica tu versión de Python
python3 --version

# Instala python-tk para tu versión (ejemplo para Python 3.14)
brew install python-tk@3.14
```
> **Nota**: Reemplaza `3.14` con tu versión de Python (ej: `3.11`, `3.12`, etc.)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update && sudo apt-get install python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3-tkinter
```

### 5. Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

### Ejecutar la aplicación GUI

```bash
cd src/GUI/src
python modulo_GUI_main.py
```

### Uso de la aplicación

1. Al iniciar, se abrirá la ventana principal
2. Haz clic en **"+ ADD IMAGES"** para seleccionar una imagen
3. Selecciona una imagen (PNG o JPG)
4. El sistema analizará la imagen y mostrará los resultados de detección

## 📦 Dependencias Principales

| Paquete | Versión | Descripción |
|---------|---------|-------------|
| `Pillow` | ≥9.0.0 | Manejo de imágenes en la GUI |
| `opencv-python` | ≥4.5.0 | Procesamiento de imágenes |
| `numpy` | ≥1.21.0 | Operaciones numéricas |
| `torch` | ≥1.10.0 | Framework de deep learning |
| `torchvision` | ≥0.11.0 | Utilidades de visión para PyTorch |

## 📁 Estructura del Proyecto

```
PySentinel/
├── README.md
├── requirements.txt
├── docs/                    # Documentación adicional
├── src/
│   ├── GUI/
│   │   ├── resource/        # Imágenes de la interfaz
│   │   └── src/             # Código de la interfaz gráfica
│   │       └── modulo_GUI_main.py  # Punto de entrada principal
│   ├── pistola/
│   │   └── detect.py        # Módulo de detección con YOLO
│   ├── general/
│   │   └── FinalCvision.py  # Funciones de visión computacional
│   ├── databases/           # Scripts de base de datos
│   └── entrenamiento/       # Dataset para entrenamiento
│       └── data/
│           ├── images/      # Imágenes de entrenamiento
│           └── label/       # Etiquetas de entrenamiento
└── yolov5-main/             # Código fuente de YOLOv5
```

## 🔧 Solución de Problemas

### Error: `ModuleNotFoundError: No module named '_tkinter'`

**Windows:**
```bash
# Reinstala Python desde python.org asegurándote de marcar "tcl/tk and IDLE" durante la instalación
# O usa el instalador de Python y selecciona "Modify" > marca "tcl/tk and IDLE"
```

**macOS (Homebrew):**
```bash
brew install python-tk@3.14  # Ajusta la versión según tu Python
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

### Error: `No module named 'cv2'`

```bash
pip install opencv-python
```

### Error: `No module named 'torch'`

```bash
pip install torch torchvision
```

## 🎯 Modelo de Detección

Actualmente el sistema usa **YOLOv5s** (modelo preentrenado general). Para detección específica de pistolas:

1. Entrena un modelo personalizado usando las imágenes en `src/entrenamiento/data/`
2. Guarda el archivo `.pt` resultante
3. Modifica `src/pistola/detect.py` para usar tu modelo personalizado

## 📄 Licencia

El proyecto puede ser modificado y utilizado para proyectos propios, mencionando las referencias a este proyecto.

## ⚡ Instalación Rápida (Copiar y Pegar)

### Windows (PowerShell o CMD)
```bash
# Crear y activar entorno virtual
python -m venv yolov5env
yolov5env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
cd src\GUI\src
python modulo_GUI_main.py
```

### macOS (Terminal)
```bash
# Instalar Tkinter (ajusta la versión de Python)
brew install python-tk@3.14

# Crear y activar entorno virtual
python3 -m venv yolov5env
source yolov5env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
cd src/GUI/src
python modulo_GUI_main.py
```

## 📚 Referencias

- [YOLOv5 - Ultralytics](https://github.com/ultralytics/yolov5)
- [OpenCV](https://opencv.org/)
- [PyTorch](https://pytorch.org/)

---

# Procedimiento para entrenar un modelo personalizado

https://www.youtube.com/watch?v=Hb5xHY4e2Mg